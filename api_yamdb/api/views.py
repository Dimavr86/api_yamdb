import uuid

from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (filters, mixins, pagination, serializers, status,
                            viewsets)
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Genre, Review, Title
from users.models import User

from api.filters import TitleFilter
from api.permissions import (AdminOnly, IsAdminOrReadOnly,
                             IsModeratororAuthororReadonly, OwnerOnly)
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, GetTokenSerializer,
                             RegUserSerializer, ReviewSerializer,
                             TitleReadSerializer, TitleWriteSerializer,
                             UserSerializer)


class CreateListDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    pass


class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = pagination.LimitOffsetPagination


class GenreViewSet(CreateListDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = pagination.LimitOffsetPagination


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Работа с отзывами."""
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsModeratororAuthororReadonly
    )
    serializer_class = ReviewSerializer
    pagination_class = pagination.LimitOffsetPagination

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        is_review_already_exist = title.reviews.filter(
            author=self.request.user
        )
        if is_review_already_exist:
            raise serializers.ValidationError(
                'Отзыв на это произведение уже существует!'
            )
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Работа с комментариями."""
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsModeratororAuthororReadonly
    )
    serializer_class = CommentSerializer

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review=review)


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = RegUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    username = serializer.validated_data['username']
    email = serializer.validated_data['email']

    if (User.objects.filter(email=email).exists()
        and User.objects.get(email=email).username != username):
            raise serializers.ValidationError(
                'Email занят другим Пользователем'
            )

    if (User.objects.filter(username=username).exists()
        and User.objects.get(username=username).email != email
        ):
            raise serializers.ValidationError(
                'Для Пользователя указан неправильный Email'
            )

    user, created = User.objects.get_or_create(
        username=username,
        email=email
    )

    if user is None and created is not None:
        user = created

    conformation_code = default_token_generator.make_token(user)
    send_mail(f'Здравствуйте {username}! Ваш код: ',
              conformation_code,
              settings.EMAIL_LETTERS,
              [email])

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    serializer = GetTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data['username']
    confirmation_code = serializer.validated_data['confirmation_code']

    user = get_object_or_404(User, username=username)
    confirmation_code = default_token_generator.make_token(user)

    if user is None:
        raise serializers.ValidationError('Некорректный Пользователь')

    if confirmation_code is None:
        raise serializers.ValidationError('Некорректный или устаревший код')

    if default_token_generator.check_token(user, confirmation_code):
        token = str(RefreshToken.for_user(user).access_token)
        response = {'token': token}
        return Response(response, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsersView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    lookup_field = 'username'
    serializer_class = UserSerializer
    permission_classes = (AdminOnly,)

    @action(detail=False, methods=['get', 'patch'],
            permission_classes=(IsAuthenticated, OwnerOnly))
    def me(self, request):
        user = get_object_or_404(User, username=self.request.user.username)
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = self.get_serializer(user,
                                         data=request.data,
                                         partial=True)

        serializer.is_valid(raise_exception=True)
  
        return Response(serializer.data, status=status.HTTP_200_OK)

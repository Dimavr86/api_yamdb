from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .permissions import AdminOnly, OwnerOnly
from .serializers import GetTokenSerializer, RegUserSerializer, UserSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = RegUserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    if not User.objects.filter(username=request.data['username'],
                               email=request.data['email']).exists():
        serializer.save()
    user = User.objects.get(username=request.data['username'],
                            email=request.data['email'])
    conformation_code = default_token_generator.make_token(user)
    send_mail(f'Здравствуйте {str(user.username)}! Ваш код: ',
              conformation_code,
              settings.EMAIL_LETTERS,
              [request.data['email']])
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    serializer = GetTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(User, username=request.data['username'])
    confirmation_code = request.data['confirmation_code']
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

        if serializer.is_valid():
            if 'role' in request.data:
                if user.role != 'user':
                    serializer.save()
            else:
                serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

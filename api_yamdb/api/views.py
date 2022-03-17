from django.shortcuts import render
from django.db.models import Avg
from rest_framework import filters, mixins, viewsets
from django_filters.rest_framework import DjangoFilterBackend

from reviews.models import Category, Genre, Title
from .serializers import (CategorySerializer,
                          GenreSerializer, TitlesSafeMethodSerializer,
                          TitlesUnSafeMethodSerializer)

class CreateListDestroyViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                             mixins.DestroyModelMixin,
                             viewsets.GenericViewSet):
    pass


class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)
    # permission_classes = (IsAdminOrReadOnly, IsSuperuser,)


class GenreViewSet(CreateListDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    # permission_classes = (IsAdminOrReadOnly | IsSuperuser,)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    # permission_classes = [IsAdminOrReadOnly]
    filter_backends = (filters.SearchFilter,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitlesSafeMethodSerializer
        return TitlesUnSafeMethodSerializer

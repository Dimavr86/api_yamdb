from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ReviewSet, CommentSet

router = DefaultRouter()
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)',
    ReviewSet,
    basename='review'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentSet,
    basename='comments'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments/(?P<comment_id>\d+)',
    CommentSet,
    basename='comment'
)


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
]
from rest_framework import routers

from .views import (CategorieViewSet, GenreViewSet,
                    TitleViewSet)

app_name = 'api'

router_v1 = routers.DefaultRouter()
router_v1.register('categories', CategorieViewSet)
router_v1.register('genres', GenreViewSet)
router_v1.register('titles', TitleViewSet)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UsersView, get_token, register_user

router_v1 = DefaultRouter()
router_v1.register('users', UsersView)

authpatterns = [
    path('signup/', register_user),
    path('token/', get_token),
    path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),
]

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/', include(authpatterns)),
]

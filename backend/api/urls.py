from django.urls import include, path
from djoser.views import UserViewSet
from rest_framework.routers import DefaultRouter

from api.views import (ColorViewSet, DocumentsViewSet, FontViewSet,
                       UserProfileDocumentViewSet, regist_user, reset_password,
                       send_reset_code, confirm_or_reset_code)

app_name = 'api'
router = DefaultRouter()
router.register('colors', ColorViewSet)
router.register('documents', DocumentsViewSet)
router.register('font', FontViewSet)
router.register('profile', UserProfileDocumentViewSet, basename='profile')

user_router = DefaultRouter()
user_router.register("users", UserViewSet, basename="users")


def is_route_selected(url_pattern):

    urls = [
        'users/me/',
    ]

    for u in urls:
        match = url_pattern.resolve(u)
        if match:
            return True
    return False


# Filter router URLs removing unwanted ones
selected_user_routes = list(filter(is_route_selected, user_router.urls))

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
    path('auth/send_reset_code/', send_reset_code),
    path('auth/reset_password/', reset_password),
    path('auth/regist/', regist_user),  # регистрация пользователя
    path('auth/confirm/', confirm_or_reset_code),  # подтверждение почты или
                                                   # сброс пароля
] + selected_user_routes

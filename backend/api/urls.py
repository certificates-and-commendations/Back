from django.urls import include, path
from djoser.views import UserViewSet
from rest_framework.routers import DefaultRouter

from api.views import (DocumentsViewSet, FavouriteViewSet, FontViewSet,
                       confirm_code, regist_user, reset_code, reset_password,
                       send_reset_code)

app_name = 'api'
router = DefaultRouter()
router.register("users/favourite", FavouriteViewSet)
router.register('documents', DocumentsViewSet)
router.register('font', FontViewSet)

user_router = DefaultRouter()
user_router.register("users", UserViewSet, basename="users")


def is_route_selected(url_pattern):

    urls = [
        'users/',
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
    # path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('auth/send_reset_code/', send_reset_code),
    path('auth/reset_code/', reset_code),
    path('auth/reset_password/', reset_password),
    path('auth/regist/', regist_user),  # регистрация пользователя
    path('auth/confirm/', confirm_code),  # подтверждение почты
] + selected_user_routes

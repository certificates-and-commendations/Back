from api.views import regist_user, confirm_code
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import FavouriteViewSet, UserViewSet, DocumentsViewSet

app_name = 'api'
router = DefaultRouter()
router.register("users/favourite", FavouriteViewSet)
router.register("users", UserViewSet)
router.register('documents', DocumentsViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('auth/regist/', regist_user),  # регистрация пользователя
    path('auth/confirm/', confirm_code),  # подтверждение почты
]

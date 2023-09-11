from api.views import (DocumentsViewSet, FavouriteViewSet, FontViewSet,
                       UserViewSet, confirm_code, regist_user)
from django.urls import include, path
from rest_framework.routers import DefaultRouter

app_name = 'api'
router = DefaultRouter()
router.register("users/favourite", FavouriteViewSet)
router.register("users", UserViewSet)
router.register('documents', DocumentsViewSet)
router.register('font', FontViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('auth/regist/', regist_user),  # регистрация пользователя
    path('auth/confirm/', confirm_code),  # подтверждение почты
]

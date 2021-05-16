from django.urls import path, include
from rest_framework import routers
from .views import UserProfileViewSet, UserHistoryViewset
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


router = routers.DefaultRouter()
router.register('profile', UserProfileViewSet, basename="registraton")
router.register('userhistory', UserHistoryViewset, basename="userhistory")


urlpatterns = [
    path('', include(router.urls)),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('', include(router.urls))
]

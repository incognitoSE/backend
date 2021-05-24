from django.urls import path, include
from rest_framework import routers
from .views import UserProfileViewSet, UserHistoryViewset, UserProfile, UserSignup, UserWalletViewset
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


router = routers.DefaultRouter()
# router.register('profile', UserProfileViewSet, basename="registraton")
router.register('userhistory', UserHistoryViewset, basename="userhistory")
router.register('userwallet', UserWalletViewset, basename="userwallet")


urlpatterns = [
    path('', include(router.urls)),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('', include(router.urls)),
    path('profile/', UserSignup.as_view(), name="registration")
]

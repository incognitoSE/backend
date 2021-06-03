from django.contrib.auth import views as auth_views
from django.urls import path, include, re_path
from rest_framework import routers
from .views import UserHistoryViewset, UserProfileViewSet, UserSignup, UserWalletViewset,\
    UserTransactionsViewset, NotificationsViewset
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


router = routers.DefaultRouter()
# router.register('profile', UserProfileViewSet, basename="registraton")
router.register('userhistory', UserHistoryViewset, basename="userhistory")
router.register('userwallet', UserWalletViewset, basename="userwallet")
router.register("usertransactions", UserTransactionsViewset, basename="usertransactions")
router.register("notifications", NotificationsViewset, basename="notifications")
router.register("changepassword", UserProfileViewSet, basename="userprofile")


urlpatterns = [
    path('', include(router.urls)),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('', include(router.urls)),
    path('profile/', UserSignup.as_view(), name="registration"),
    path('', include('django.contrib.auth.urls')),

    # path("password_reset", password_reset_request, name="password_reset")

]

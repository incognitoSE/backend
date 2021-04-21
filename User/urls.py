from django.urls import path, include
from rest_framework import routers
from .views import UserProfileViewSet, LoginView


router = routers.DefaultRouter()
router.register('profile', UserProfileViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view())
]

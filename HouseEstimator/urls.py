from django.urls import path, include
from rest_framework import routers
from .views import Houseview


router = routers.DefaultRouter()
router.register('api', Houseview, basename="HouseEstimatorViewSet")


urlpatterns = [
    path('', include(router.urls)),
]

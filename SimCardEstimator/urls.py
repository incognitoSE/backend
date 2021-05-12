from django.urls import path, include
from rest_framework import routers
from .views import SimcardView

router = routers.DefaultRouter()
router.register('Simcard', SimcardView, basename="SimcardEstimatorViewSet")

urlpatterns = [
    path('', include(router.urls)),
]
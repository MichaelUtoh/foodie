from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .api import PaymentViewSet

app_name = "payments"

router = DefaultRouter()
router.register("", PaymentViewSet, basename="payments")


urlpatterns = [
    path("", include(router.urls)),
]

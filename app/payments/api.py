from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Payment
from .serializers import PaymentCreateSerializer, PaymentListSerializer
from core.utils import filter_http_method_names


class PaymentViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Payment.objects.all().order_by()
    # http_method_names = filter_http_method_names(["patch", "put"])

    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return PaymentListSerializer
        if self.action == "initiate" or self.action == "update":
            return PaymentCreateSerializer

    @swagger_auto_schema(
        request_body=PaymentCreateSerializer,
        responses={status.HTTP_200_OK: PaymentListSerializer},
    )
    @action(detail=False, methods=["POST"], url_path="initiate")
    def initiate(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        payment = serializer.save()
        data = PaymentListSerializer(payment).data
        return Response(data=data)

from rest_framework import serializers

from accounts.models import User
from .models import Payment
from .utils import (
    _generate_reference_code,
    _initiate_transaction,
    _is_valid_reference,
    _verify_transaction,
)


class PaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "invoice_id",
            "user",
            "invoice_id",
            "reference",
            "payment_gateway",
            "total_amount",
        ]

    def create(self, validated_data):
        try:
            user = validated_data["user"]
            amount = float(validated_data["total_amount"])
            reference = (
                validated_data.get("referrence", None) or _generate_reference_code()
            )

            if _is_valid_reference(reference):
                authorization_url = _initiate_transaction(user.email, amount, reference)
                payment = Payment.objects.create(**validated_data)
                payment.authorization_url = authorization_url
                payment.save()
                return payment
        except Exception as e:
            raise serializers.ValidationError(
                f"Payment processing was unsuccessful, {e}"
            )


class PaymentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "id",
            "invoice_id",
            "user",
            "invoice_id",
            "reference",
            "payment_gateway",
            "authorization_url",
            "status",
            "metadata",
            "total_amount",
        ]

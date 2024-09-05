import uuid
from enum import Enum

from django.db import models
from django.conf import settings

from core.base import Base


class PaymentStatus(models.TextChoices):
    SUCCESS = "success", "Success"
    FAILED = "failed", "Failed"
    REVERSED = "reversed", "Reversed"
    PENDING = "pending", "Pending"

    def __str__(self):
        return self.value


class Payment(Base):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    invoice_id = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="payments",
    )
    invoice_id = models.CharField(max_length=255)
    reference = models.CharField(max_length=255, blank=True)
    payment_gateway = models.CharField(max_length=255, blank=True)
    authorization_url = models.CharField(max_length=255, blank=True)
    status = models.CharField(
        max_length=255,
        choices=PaymentStatus,
        default=PaymentStatus.PENDING.value,
    )
    metadata = models.JSONField(null=True, blank=True)
    total_amount = models.DecimalField(max_digits=14, default=0, decimal_places=2)

    def __str__(self):
        return f"{self.invoice_id} - {self.reference}"

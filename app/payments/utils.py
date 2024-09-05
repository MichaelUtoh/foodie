import os
import logging
import random
import string

import requests
from django.conf import settings
from django.shortcuts import get_object_or_404
from paystackapi.transaction import Transaction

from .models import Payment


PAYSTACK_SECRET_KEY = settings.PAYSTACK_SECRET_KEY
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)


def _initiate_transaction(email, amount, reference):
    try:
        response = Transaction.initialize(
            email=email,
            amount=amount * 100,
            reference=reference,
        )
        if response["status"]:
            authorization_url = response["data"]["authorization_url"]
            return authorization_url
        else:
            raise Exception(f"Payment initiation failed: {response['message']}")
    except Exception as e:
        LOGGER.info(f"An error occured: {e}")
        raise e


def _verify_transaction(reference):
    url = f"https://api.paystack.co/transaction/verify/{reference}"
    headers = {
        "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json",
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        verification_data = response.json()
        if (
            verification_data.get("status")
            and verification_data["data"]["status"] == "success"
        ):
            return verification_data.get("data")
        else:
            raise ValueError("Transaction verification failed")
    else:
        response.raise_for_status()


def _generate_reference_code(prefix="PAY"):
    digits = "".join(random.choices(string.digits, k=2))
    letter = random.choice(string.ascii_uppercase)
    more_digits = "".join(random.choices(string.digits, k=2))
    return f"{prefix}{digits}{letter}{more_digits}"


def _is_valid_reference(code):
    LOGGER.info(f"finding payment for reference: {code}")
    payment_ref_exists = Payment.objects.filter(reference=code)
    if payment_ref_exists:
        return False
    return True

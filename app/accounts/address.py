from django.db import models
from django.core.exceptions import ValidationError

from core.base import Base


class State(Base):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Lga(Base):
    name = models.CharField(max_length=255)
    state = models.ForeignKey(State, related_name="lgas", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Address(Base):
    city = models.CharField(max_length=255, blank=True)
    street = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name

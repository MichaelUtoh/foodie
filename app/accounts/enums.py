from django.db import models


class Gender(models.TextChoices):
    MALE = "M", "Male"
    FEMALE = "F", "Female"
    OTHERS = "O", "Others"


class Title(models.TextChoices):
    MR = "Mr", "Mr"
    MRS = "Mrs", "Mrs"
    MISS = "Miss", "Miss"


class UserRole(models.TextChoices):
    ADMIN = "admin", "Admin"
    BUYER = "buyer", "Buyer"
    DISPATCH = "dispatch", "Dispatch"
    SELLER = "seller", "Seller"


class UserStatus(models.TextChoices):
    ACTIVE = "active", "Active"
    INACTIVE = "inactive", "Inactive"
    PENDING = "pending", "Pending"
    SUSPENDED = "suspended", "Suspended"

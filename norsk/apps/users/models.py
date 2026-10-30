from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("username",)


class UserOwnedModel(models.Model):
    """
    Abstract base model for models that are owned by a user.
    """

    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="%(class)ss"
    )

    class Meta:
        abstract = True

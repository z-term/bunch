import uuid
from typing import override

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class User(AbstractUser):
    """
    Custom User Model for bunch.
    Adds additional properties like avatar, status, bio etc..
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=False, help_text="User's profile picture")
    status = models.CharField(blank=True, null=True, max_length=30, help_text="User's status")
    bio = models.TextField(blank=True, null=True, help_text="User's bio")

    @override
    def __str__(self) -> str:
        return self.username

    @override
    def clean(self):
        if not self.email:
            raise ValidationError("Email is required.")

        super().clean()

    @override
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

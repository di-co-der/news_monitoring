from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models import CharField
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """Custom manager where email is the unique identifier for authentication."""

    def create_user(self, email, password=None, **extra_fields):
        """Create and return a regular user with an email instead of a username."""
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", True)
        user = self.model(username=email, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a superuser with an email."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Default custom user model for news_monitoring.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore[assignment]
    last_name = None  # type: ignore[assignment]
    username = models.EmailField(unique=True)
    company = models.ForeignKey('Company', on_delete=models.CASCADE, null=True, blank=True)
    objects = CustomUserManager()  # Assign custom manager, company

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})


class Company(models.Model):
    """
    A company that users belong to.
    """
    added_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="companies_added"
    )
    updated_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="companies_updated", null=True, blank=True
    )

    name = models.CharField(max_length=255, null=False, blank=False)
    company_url = models.URLField(unique=True, null=False, blank=False)
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

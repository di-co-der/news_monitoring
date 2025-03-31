from allauth.account.forms import SignupForm
from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

from .models import User, Company

User = get_user_model()

class UserAdminChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = "__all__"


class UserAdminCreationForm(UserCreationForm):
    """
    Form for User Creation in the Admin Area.
    """

    class Meta:
        model = User
        fields = ("username", "password1", "password2")
        error_messages = {
            "username": {"unique": _("This email is already in use.")},
        }


class UserSignupForm(SignupForm):
    """
    Form for user sign-up.
    """

    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(),
    )
    company_name = forms.CharField(
        label="Company Name",
        widget=forms.TextInput(),
        required=True  # Ensure this field is required
    )
    company_url = forms.URLField(
        label="Company URL",
        widget=forms.URLInput(),
        required=True
    )

    def clean_email(self):
        """Ensure email is unique since it's used as username."""
        email = self.cleaned_data.get("email")
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email

    def clean_company_name(self):
        """Ensure the company exists in the database before proceeding."""
        company_name = self.cleaned_data.get("company_name")
        if not Company.objects.filter(name=company_name).exists():
            raise forms.ValidationError("This company is not registered.")
        return company_name

    def save(self, request):
        """Save user with email as username and associate with a company."""
        user = super().save(request)
        email = self.cleaned_data.get("email")
        company_name = self.cleaned_data.get("company_name")
        company_url = self.cleaned_data.get("company_url")

        # Set email as username
        user.username = email
        user.save()

        # Ensure company exists or create one
        company, created = Company.objects.get_or_create(
            name=company_name,
            defaults={"company_url": company_url}
        )

        user.company = company
        user.save()
        return user

class UserSocialSignupForm(SocialSignupForm):
    """
    Form when user signs up via social authentication.
    """

from allauth.account.forms import SignupForm
from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from allauth.account.views import SignupView

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
    company_name = forms.ModelChoiceField(
        label="Company Name",
        queryset=Company.objects.all(),
        empty_label="Select a Company",
        required=True  # Ensure this field is required
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove the username field if it exists
        if 'username' in self.fields:
            del self.fields['username']

    def clean_email(self):
        """Ensure email is unique since it's used as username."""
        email = self.cleaned_data.get("email")
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email

    def save(self, request):
        """Save user with email as username and associate with a company."""
        user = super().save(request)
        email = self.cleaned_data.get("email")
        company_name = self.cleaned_data.get("company_name")

        # Set email as username
        user.username = email
        user.email = email
        user.company = company_name
        user.save()

        return user

class UserSocialSignupForm(SocialSignupForm):
    """
    Form when user signs up via social authentication.
    """

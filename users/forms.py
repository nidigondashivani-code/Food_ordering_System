from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "phone",
            "role",
            "address",
            "profile_image",
            "profile_image_url",
        ]

        widgets = {
            "first_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "First Name",
            }),
            "last_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Last Name",
            }),
            "username": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Username",
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "Email Address",
            }),
            "phone": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "10-digit Phone Number",
            }),
            "role": forms.Select(attrs={
                "class": "form-control",
            }),
            "address": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Complete Delivery Address",
            }),
            "profile_image": forms.FileInput(attrs={
                "class": "form-control",
                "accept": "image/*",
            }),
            "profile_image_url": forms.URLInput(attrs={
                "class": "form-control",
                "placeholder": "Or Paste Web Profile Image Link (https://...)",
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["password1"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Password",
        })

        self.fields["password2"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Confirm Password",
        })


class OwnerRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "phone",
            "address",
            "profile_image",
            "profile_image_url",
        ]

        widgets = {
            "first_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "First Name",
            }),
            "last_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Last Name",
            }),
            "username": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Username",
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "Email Address",
            }),
            "phone": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "10-digit Phone Number",
            }),
            "address": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Restaurant / Owner Address",
            }),
            "profile_image": forms.FileInput(attrs={
                "class": "form-control",
                "accept": "image/*",
            }),
            "profile_image_url": forms.URLInput(attrs={
                "class": "form-control",
                "placeholder": "Or Paste Web Profile Image Link (https://...)",
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["password1"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Password",
        })

        self.fields["password2"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Confirm Password",
        })

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = "restaurant"
        if commit:
            user.save()
        return user
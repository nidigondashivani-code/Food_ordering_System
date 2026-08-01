from django import forms
from .models import Restaurant


class RestaurantRegistrationForm(forms.ModelForm):

    class Meta:
        model = Restaurant

        exclude = (
            "owner",
            "status",
            "rating",
            "created_at",
        )

        widgets = {
            "restaurant_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Restaurant Name"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Brief description"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "Contact Phone"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Contact Email"}),
            "address": forms.Textarea(attrs={"class": "form-control", "rows": 2, "placeholder": "Street Address"}),
            "city": forms.TextInput(attrs={"class": "form-control", "placeholder": "City"}),
            "state": forms.TextInput(attrs={"class": "form-control", "placeholder": "State"}),
            "pincode": forms.TextInput(attrs={"class": "form-control", "placeholder": "Pincode"}),
            "cuisine": forms.TextInput(attrs={"class": "form-control", "placeholder": "Cuisine type (e.g. Indian, Italian)"}),
            "opening_time": forms.TimeInput(attrs={"class": "form-control", "type": "time"}),
            "closing_time": forms.TimeInput(attrs={"class": "form-control", "type": "time"}),
            "minimum_order": forms.NumberInput(attrs={"class": "form-control"}),
            "delivery_time": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Minutes"}),
            "logo": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "logo_url": forms.URLInput(attrs={"class": "form-control", "placeholder": "Or Paste Logo Image URL (https://...)"}),
            "cover_image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "cover_image_url": forms.URLInput(attrs={"class": "form-control", "placeholder": "Or Paste Cover Image URL (https://...)"}),
            "fssai_license": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "gst_number": forms.TextInput(attrs={"class": "form-control", "placeholder": "GSTIN Number"}),
        }
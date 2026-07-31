from django import forms
from .models import MenuItem


class MenuItemForm(forms.ModelForm):

    class Meta:
        model = MenuItem

        exclude = (
            "restaurant",
            "created_at",
        )

        widgets = {

            "food_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter food name"
            }),

            "category": forms.Select(attrs={
                "class": "form-control"
            }),

            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Food description"
            }),

            "price": forms.NumberInput(attrs={
                "class": "form-control"
            }),

            "calories": forms.NumberInput(attrs={
                "class": "form-control"
            }),

            "protein": forms.NumberInput(attrs={
                "class": "form-control"
            }),

            "carbs": forms.NumberInput(attrs={
                "class": "form-control"
            }),

            "fat": forms.NumberInput(attrs={
                "class": "form-control"
            }),

            "preparation_time": forms.NumberInput(attrs={
                "class": "form-control"
            }),

            "image": forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),

            "is_veg": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),

            "is_available": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),

            "is_popular": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),
        }
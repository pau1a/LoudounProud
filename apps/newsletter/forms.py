from django import forms

from .models import Subscriber


class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ["email", "first_name"]
        widgets = {
            "email": forms.EmailInput(attrs={
                "placeholder": "Your email address",
                "class": "subscribe-form__input",
            }),
            "first_name": forms.TextInput(attrs={
                "placeholder": "First name (optional)",
                "class": "subscribe-form__input",
            }),
        }

    def clean_email(self):
        email = self.cleaned_data["email"].lower().strip()
        existing = Subscriber.objects.filter(email=email).first()
        if existing and existing.is_confirmed:
            raise forms.ValidationError("This email is already subscribed.")
        return email

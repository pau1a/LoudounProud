from django import forms

from .models import AdvertiserLead


class AdvertiserLeadForm(forms.ModelForm):
    website = forms.CharField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = AdvertiserLead
        fields = [
            "name",
            "business_name",
            "email",
            "phone",
            "budget_range",
            "campaign_goal",
            "message",
        ]
        widgets = {
            "name": forms.TextInput(attrs={
                "placeholder": "Your name",
                "class": "advertise-form__input",
            }),
            "business_name": forms.TextInput(attrs={
                "placeholder": "Business name",
                "class": "advertise-form__input",
            }),
            "email": forms.EmailInput(attrs={
                "placeholder": "Email address",
                "class": "advertise-form__input",
            }),
            "phone": forms.TextInput(attrs={
                "placeholder": "Phone (optional)",
                "class": "advertise-form__input",
            }),
            "budget_range": forms.Select(attrs={
                "class": "advertise-form__select",
            }),
            "campaign_goal": forms.Select(attrs={
                "class": "advertise-form__select",
            }),
            "message": forms.Textarea(attrs={
                "placeholder": "Tell us about your goals (optional)",
                "class": "advertise-form__textarea",
                "rows": 4,
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["budget_range"].choices = [("", "Budget range")] + list(
            AdvertiserLead.BUDGET_CHOICES
        )
        self.fields["campaign_goal"].choices = [("", "Campaign goal")] + list(
            AdvertiserLead.GOAL_CHOICES
        )

    def is_honeypot(self):
        return bool(self.data.get("website", "").strip())

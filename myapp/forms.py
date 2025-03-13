from django import forms
from .models import Network
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class NetworkForm(forms.ModelForm):
    class Meta:
        model = Network
        fields = '__all__'  
        widgets = {
            'host_name': forms.TextInput(attrs={'class': 'form-control'}),
            'server_1': forms.TextInput(attrs={'class': 'form-control'}),
            'server_2': forms.TextInput(attrs={'class': 'form-control'}),
            'domain_name': forms.TextInput(attrs={'class': 'form-control'}),
            'ipv4_address': forms.TextInput(attrs={'class': 'form-control'}),
            'gateway': forms.TextInput(attrs={'class': 'form-control'}),
            'ipv4_address_1': forms.TextInput(attrs={'class': 'form-control'}),
            'ntp_server': forms.TextInput(attrs={'class': 'form-control'}),
            'authentication_key': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ChangePasswordForm(forms.Form):
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'p-2 border bg-light w-100'}),
        label="New Password"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'p-2 border bg-light w-100'}),
        label="Re-Enter Password"
    )

    def clean_new_password(self):
        new_password = self.cleaned_data.get("new_password")

        try:
            validate_password(new_password)  # Use Django's built-in password validation
        except ValidationError as e:
            raise forms.ValidationError(e.messages)  # Show all validation errors

        return new_password

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError("Passwords do not match!")

        return cleaned_data

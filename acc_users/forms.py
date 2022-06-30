from django import forms
from django.forms import ModelForm
from .models import PasswordResetEmail, ChangePasswordCode, ChangePassword

class EmailPasswordReset(forms.ModelForm):
    class Meta:
        model = PasswordResetEmail
        fields = ['email']
        widgets = {
            'email':forms.EmailInput(),
        }

class ChangePasswordCodeForm(forms.ModelForm):
    class Meta:
        model = ChangePasswordCode
        fields = ['user_email']
        widgets = {
                    'user_email': forms.EmailInput(),
        }

class ChangePasswordForm(forms.ModelForm):
    class Meta:
        model = ChangePassword
        fields = ['new_password', 'confirm_new_password']
        widgets = {
                    'new_password':forms.PasswordInput(),
                    'confirm_new_password':forms.PasswordInput(),
        }



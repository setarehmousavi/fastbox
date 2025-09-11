from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

class UserRegisterationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['email', 'username', 'phone_number', 'first_name', 'last_name']
    

    def clean_password2(self):
        pass1 = self.cleaned_data.get('password')
        pass2 = self.cleaned_data.get('password2')

        if pass1 != pass2:
            raise ValidationError("Passwords Does not Match!")
        return pass2



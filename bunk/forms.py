from django import forms
from django.forms import ModelForm
from bunk.models import Bunk
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    class Meta:
        model = User
        fields = ['username', 'password']


class BunkForm(ModelForm):
    # bunk just has a from_user, to_user, and timestamp (which is auto_now_add)
    class Meta:
        model = Bunk
        fields = ["from_user", "to_user"]



class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'photo', 'password1', 'password2']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 != password2:
            raise forms.ValidationError("Passwords do not match.")


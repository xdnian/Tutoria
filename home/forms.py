from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
    
# class SignUpForm(forms.ModelForm):
#     username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username','type':'text'}))
#     password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password','type':'password'}))


class UserForm(UserCreationForm):
    identity = forms.ChoiceField(choices=Profile.IDENTITY_CHOICES)
    school = forms.CharField()
    class Meta:
        model = User
        fields = ('username','first_name', 'last_name', 'email', 'identity', 'school', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = 'enter a username'
        self.fields['school'].help_text = 'your school'
        self.fields['password1'].help_text = 'enter a password'
        self.fields['password2'].help_text = 'confirm your password'

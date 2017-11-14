from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

    
# class SignUpForm(forms.ModelForm):
#     username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username','type':'text'}))
#     password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password','type':'password'}))


class UserForm(UserCreationForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.CharField()
    phone = forms.CharField()
    identity = forms.ChoiceField(choices=Profile.IDENTITY_CHOICES)
    school = forms.ChoiceField(choices=Profile.SCHOOL_CHOICES)
    class Meta:
        model = User
        fields = ('username','first_name', 'last_name', 'email', 'phone', 'identity', 'school', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        for f in self.fields: self.fields[f].widget.attrs['class'] = 'form-control'
        self.fields['identity'].widget.attrs['class'] = 'form-control custom-select'
        self.fields['school'].widget.attrs['class'] = 'form-control custom-select'

        self.fields['username'].help_text = 'enter a username'
        self.fields['identity'].help_text = 'register as student/tutor'
        self.fields['school'].help_text = 'choose your school'
        self.fields['password1'].help_text = 'enter a password'
        self.fields['password2'].help_text = 're-enter your password'

class PasswordResetRequestForm(forms.Form):
    email = forms.CharField(label=("Email"), max_length=254, widget=forms.TextInput(attrs={'class': 'form-control'}))


class PasswordResetForm(forms.Form):
    email = forms.CharField(label=("Email"), max_length=254, widget=forms.TextInput(attrs={'class': 'form-control'}))
    token = forms.CharField(label=("Token"), max_length=254, widget=forms.TextInput(attrs={'class': 'form-control'}))
    newpassword = forms.CharField(label=("New Password"), max_length=254, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Tutorprofile

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

        for f in self.fields: 
            if self.fields[f].__class__.__name__ == 'ChoiceField':
                self.fields[f].widget.attrs['class'] = 'form-control custom-select'
            else:
                self.fields[f].widget.attrs['class'] = 'form-control'

        self.fields['username'].help_text = 'enter a username'
        self.fields['identity'].help_text = 'register as student/tutor'
        self.fields['school'].help_text = 'choose your school'
        self.fields['password1'].help_text = 'enter a password'
        self.fields['password2'].help_text = 're-enter your password'

class EditProfileForm(forms.Form):
    fields = {}
    def __init__(self, thisUser, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.user = User.objects.get(id=thisUser.id)
        self.fields['first_name'] = forms.CharField(initial=self.user.first_name)
        self.fields['last_name'] = forms.CharField(initial=self.user.last_name)
        self.fields['email'] = forms.CharField(initial=self.user.email)
        self.fields['phone'] = forms.CharField(initial=self.user.profile.phone)
        self.fields['identity'] = forms.ChoiceField(choices=Profile.IDENTITY_CHOICES, initial=self.user.profile.identity)
        self.fields['school'] = forms.ChoiceField(choices=Profile.SCHOOL_CHOICES, initial=self.user.profile.school)
        self.fields['bank_account'] = forms.CharField(initial=self.user.profile.wallet.bank_account, required=False)
        if self.user.profile.identity == 'T':
            self.fields['tutortype'] = forms.ChoiceField(choices=Tutorprofile.TUTOR_CHOICES, initial=self.user.tutorprofile.tutortype)
            self.fields['courses'] = forms.CharField(initial=self.user.tutorprofile.courses, required=False)
            self.fields['biography'] = forms.CharField(initial=self.user.tutorprofile.biography, required=False, widget=forms.Textarea(attrs={'rows':3})) 
            self.fields['subjects'] = forms.CharField(initial=self.user.tutorprofile.subjects, required=False)
            self.fields['price'] = forms.DecimalField(initial=self.user.tutorprofile.price, widget=forms.NumberInput(attrs={'step':10, 'min':0}))
            self.fields['price'].help_text = 'must be a multiple of 10'

        for f in self.fields: 
            if self.fields[f].__class__.__name__ == 'ChoiceField':
                self.fields[f].widget.attrs['class'] = 'form-control-plaintext custom-select'
                self.fields[f].widget.attrs['disabled'] = ''
            else:
                self.fields[f].widget.attrs['class'] = 'form-control-plaintext'
                self.fields[f].widget.attrs['readonly'] = ''

    def save(self):
        self.user.first_name = self.cleaned_data['first_name']
        self.user.last_name = self.cleaned_data['last_name']
        self.user.profile.email = self.cleaned_data['email']
        self.user.profile.phone = self.cleaned_data['phone']
        self.user.profile.identity = self.cleaned_data['identity']
        self.user.profile.school = self.cleaned_data['school']
        self.user.profile.wallet.bank_account = self.cleaned_data['bank_account']
        if self.user.profile.identity == 'T':
            self.user.tutorprofile.tutortype = self.cleaned_data['tutortype']
            self.user.tutorprofile.courses = self.cleaned_data['courses']
            self.user.tutorprofile.biography = self.cleaned_data['biography']
            self.user.tutorprofile.subjects = self.cleaned_data['subjects']
            if self.user.tutorprofile.tutortype == 'C':
                self.user.tutorprofile.price = decimal.Decimal(0.00)
            else:
                self.user.tutorprofile.price = self.cleaned_data['price']
        self.user.save()
        self.user.profile.save()
        self.user.profile.wallet.save()
        self.user.tutorprofile.save()

class ChangePasswordForm(forms.Form):
    newpassword = forms.CharField(label=("New Password"), max_length=254, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_newpassword = forms.CharField(label=("Confirm New Password"), max_length=254, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
        
class PasswordResetRequestForm(forms.Form):
    email = forms.CharField(label=("Email"), max_length=254, widget=forms.TextInput(attrs={'class': 'form-control'}))

class PasswordResetForm(forms.Form):
    email = forms.CharField(label=("Email"), max_length=254, widget=forms.TextInput(attrs={'class': 'form-control'}))
    token = forms.CharField(label=("Token"), max_length=254, widget=forms.TextInput(attrs={'class': 'form-control'}))
    newpassword = forms.CharField(label=("New Password"), max_length=254, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

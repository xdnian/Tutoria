from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_control
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import UserForm, PasswordResetRequestForm, PasswordResetForm, EditProfileForm, ChangePasswordForm
from .models import Reset_token, Notification
from transaction.models import Wallet
from uuid import uuid4
from django.template import RequestContext

import os

@login_required
def home(request):
    return render(request, 'overview.html')


def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.phone = form.cleaned_data.get('phone')
            user.profile.identity = form.cleaned_data.get('identity')
            user.profile.school = form.cleaned_data.get('school')
            user.save()
            
            # create wallet and assosiate it to the user
            newWallet = Wallet(user = user, balance = 0)
            newWallet.save()
            user.profile.wallet = newWallet
            user.save()
            
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def editProfile(request):
    save_msg = None
    if request.method == 'POST':
        form = EditProfileForm(request.user, request.POST, request.FILES)
        if form.is_valid():
            form.save()
            save_msg = {'error': False, 'msg': 'Your edit has been saved.'}
        else:
            save_msg = {'error': True, 'msg': 'Error when saving your edit. Please try again.'}
    else:
        form = EditProfileForm(request.user)
    return render(request, 'profile.html', {'form': form, 'save_msg': save_msg})

def passwordResetRequest(request):
    instruct = 'Please enter the email you used for Tutoria account to receive token.'
    button_text = 'Send'
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            this_user = User.objects.filter(email=email)
            if len(this_user) != 0:
                rand_token = uuid4()
                reset_token = Reset_token(user=this_user[0], token=str(rand_token))
                reset_token.save()
                Notification(this_user[0], 'Use this token to reset your password: ' + str(rand_token))
                return redirect('passwordReset')
            else:
                form = PasswordResetRequestForm()
                return render(request, 'password-reset.html', {'form': form, 'instruct': instruct, 'button_text': button_text, 'message': 'This email does not exist.'})
    else:
        form = PasswordResetRequestForm()
    return render(request, 'password-reset.html', {'form': form, 'instruct': instruct, 'button_text': button_text})

def validate_password_strength(value):
    """a password is as least 8 characters long and contains both numbers and letters.
    """
    min_length = 8

    if len(value) < min_length:
        return False

    # check for letters
    if sum(c.isdigit() for c in value) == len(value):
        return False

    # check for digits
    if sum(not c.isdigit() for c in value) == len(value):
        return False

    return True

def passwordReset(request):
    instruct = 'Please enter the email, token and set your new password.'
    button_text = 'Confirm'
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            token = form.cleaned_data.get('token')
            newpassword = form.cleaned_data.get('newpassword')
            validation = validate_password_strength(newpassword)
            this_user = User.objects.filter(email=email)
            if len(this_user) != 0:
                related_token = Reset_token.objects.filter(user=this_user[0])
                if len(related_token) != 0 and related_token[0].token == token:
                    u = User.objects.get(username=this_user[0].username)
                    if validation:
                        u.set_password(newpassword)
                        u.save()
                        related_token.delete()
                        button = {'label':'Confirm', 'link': '/'}
                        return_msg = {'success': True, 'msg': 'Your password has been reset sucessfully.', 'button': button}
                        return render(request, 'account-result.html', {'return_msg': return_msg})
                    else:
                        form = PasswordResetForm()
                        return render(request, 'password-reset.html', {'form': form, 'instruct': instruct, 'button_text': button_text, 'message': 'a password is as least 8 characters long and contains both numbers and letters'})
                else:
                    form = PasswordResetForm()
                    return render(request, 'password-reset.html', {'form': form, 'instruct': instruct, 'button_text': button_text, 'message': 'Wrong token'})
            else:
                form = PasswordResetForm()
                return render(request, 'password-reset.html', {'form': form, 'instruct': instruct, 'button_text': button_text, 'message': 'Wrong email'})
    else:
        form = PasswordResetForm()
    return render(request, 'password-reset.html', {'form': form, 'instruct': instruct, 'button_text': button_text})

@login_required
def changePassword(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            newpassword = form.cleaned_data.get('newpassword')
            confirm_newpassword = form.cleaned_data.get('confirm_newpassword')
            if newpassword != confirm_newpassword:
                form = ChangePasswordForm()
                return render(request, 'change-password.html', {'form': form, 'message': 'The two passwords do not match, please enter again.'})
            else:
                validation = validate_password_strength(newpassword)
                if validation:
                    u = request.user
                    u.set_password(newpassword)
                    u.save()
                    button = {'label':'Log in', 'link': '/login/'}
                    return_msg = {'success': True, 'msg': 'Your password has been reset sucessfully.', 'button': button}
                    return render(request, 'account-result.html', {'return_msg': return_msg})
                else:
                    form = ChangePasswordForm()
                    return render(request, 'change-password.html', {'form': form, 'message': 'a password is as least 8 characters long and contains both numbers and letters'})
    else:
        form = ChangePasswordForm()
    return render(request, 'change-password.html', {'form': form})

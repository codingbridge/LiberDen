from django.contrib import messages
from django.contrib.auth import get_user_model, login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm, SetPasswordForm
from .forms import AuthenticateForm, UserCreateForm, UserEditForm


def signup_view(request, form=None):
    form = UserCreateForm()
    if request.method == 'POST':
        form = UserCreateForm(data=request.POST)
        if form.is_valid():
            username = form["username"].data
            password = form["password2"].data
            form.save()
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('library')
        else:
            messages.error(request, form.errors)
    return render(request, 'signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('library')

def signin_view(request, form=None):
    if request.user.is_authenticated:
        redirect('library')
    if request.method == 'POST':
        form = AuthenticateForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('library')
        else:
            messages.error(request, "username or password not correct")
    else:
        form = AuthenticateForm()
    return render(request, 'users/signin.html', {'form': form})

@login_required
def edituser_view(request, form=None):    
    if request.method == 'POST':
        form = UserEditForm(data=request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was successfully updated!')
        else:
            return edituser_view(request, form=form)
    form = UserEditForm(instance=request.user)    
    return render(request, 'users/settings.html', {'form': form})

@login_required
def changepassword_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
        else:            
            messages.error(request, form.errors)
    form = PasswordChangeForm(request.user)
    return render(request, 'users/changepassword.html', { 'form': form })

def forgotpassword_view(request, form=None):
    if request.method == 'POST':
        form = PasswordResetForm()
        if form.is_valid():
            form.save(from_email="myemailaddress@abc.com", email_template_name="\\users\\passwordresetemail.html")
            messages.success(request, 'An email has been sent to ' + form.cleaned_data["email"])
        else:            
            messages.error(request, form.errors)
    form = PasswordResetForm()
    return render(request, 'users/forgotpassword.html', { 'form': form })

def resetpassword_view(request, uid, token):    
    form = SetPasswordForm(user=request.user, data=request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Your password has been reset successfully!')
    else:
        messages.error(request, form.errors)
    return render(request, 'users/resetpassword.html', { 'form': form })
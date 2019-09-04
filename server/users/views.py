from django.contrib.auth import get_user_model, login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from .forms import AuthenticateForm, UserCreateForm, UserEditForm


def signup_view(request, form=None):
    if request.method == 'POST':
        form = UserCreateForm(data=request.POST)
        if form.is_valid():
            username = form.clean_username()
            password = form.clean_password2()
            form.save()
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('library')
        else:
            return signup_view(request, form=form)
    form = UserCreateForm()    
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
            form = form or AuthenticateForm()
            return render(request, 'signin.html', {'form': form})
    form = AuthenticateForm()
    return render(request, 'signin.html', {'form': form})

@login_required
def edituser_view(request, form=None):    
    if request.method == 'POST':
        form = UserEditForm(data=request.POST, instance=request.user)
        if form.is_valid():
            form.save()
        else:
            return edituser_view(request, form=form)
    form = UserEditForm(instance=request.user)    
    return render(request, 'settings.html', {'form': form})

@login_required
def changepassword_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            return redirect('changepassword_view')
    form = PasswordChangeForm(request.user)
    return render(request, 'changepassword.html', { 'form': form })

def forgotpassword_view(request, form=None):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            # user = form.save()
            # update_session_auth_hash(request, user)  # Important!
            # messages.success(request, 'Your password was successfully updated!')
            return redirect('forgotpassword_view')
    form = PasswordResetForm()
    return render(request, 'forgotpassword.html', { 'form': form })

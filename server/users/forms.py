
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from django.utils.html import strip_tags
from .models import UserProfile, User
#from .models import UserProfile, User, Author, Publisher, LendPeriods, Book
from django.utils import timezone
#from django.forms import ModelForm


class UserCreateForm(UserCreationForm):
    """
    Form for creation user instances
    """
    username = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Username','class': "form-control"}))
    first_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'First Name','class': "form-control"}))
    last_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Last Name','class': "form-control"}))
    password1 = forms.CharField(required=True, widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Password','class': "form-control"}))
    password2 = forms.CharField(required=True,
                                widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Password Confirmation','class': "form-control"}))

    def is_valid(self):
        form = super(UserCreateForm, self).is_valid()
        for f, error in self.errors.iteritems():
            if f != '__all_':
                self.fields[f].widget.attrs.update({'class': 'error', 'value': strip_tags(error)})
        return form

    def save(self):
        user = super(UserCreateForm, self).save()
        user_profile = UserProfile(user=user, join_date=timezone.now())
        user_profile.save()
        return user_profile

    class Meta:
        fields = ['username', 'first_name', 'last_name', 'password1',
                  'password2']
        model = User


class AuthenticateForm(AuthenticationForm):
    """
    Form to authenticate user
    """
    username = forms.CharField(widget=forms.widgets.TextInput(attrs={'placeholder': 'Username','class': "form-control"}))
    password = forms.CharField(widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Password','class': "form-control"}))

    def is_valid(self):
        form = super(AuthenticateForm, self).is_valid()
        for f, error in self.errors.iteritems():
            if f != '__all__':
                self.fields[f].widget.attrs.update({'class': 'error', 'value': strip_tags(error)})
        return form
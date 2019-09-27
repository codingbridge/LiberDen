# pylint: disable=missing-docstring
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.utils.html import strip_tags
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator

PHONE_VALIDATOR = RegexValidator(r"^(?:\+?86)?1(?:3\d{3}|5[^4\D]\d{2}|8\d{3}|7(?:[35678]\d{2}|\
                                 4(?:0\d|1[0-2]|9\d))|9[189]\d{2}|66\d{2})\d{6}$",
                                 "phone number is not valid.")
USER = get_user_model()


class UserCreateForm(UserCreationForm):
    username = forms.CharField(required=True,
                               widget=forms.widgets.TextInput(
                                   attrs={'placeholder': 'Username', 'class': "form-control"}))
    mobile = forms.CharField(required=True,
                             widget=forms.widgets.TextInput(
                                 attrs={'placeholder': 'mobile phone', 'class': "form-control"}),
                             validators=[])
    password1 = forms.CharField(required=True,
                                widget=forms.widgets.PasswordInput(
                                    attrs={'placeholder': 'Password', 'class': "form-control"}))
    password2 = forms.CharField(required=True,
                                widget=forms.widgets.PasswordInput(
                                    attrs={'placeholder': 'Password Confirmation',
                                           'class': "form-control"}))


    def is_valid(self):
        form = super(UserCreateForm, self).is_valid()
        for field, error in self.errors.items():
            if field != '__all_':
                self.fields[field].widget.attrs.update(
                    {'class': 'error', 'value': strip_tags(error)})
        return form

    class Meta:
        fields = ['username', 'password1', 'password2', 'mobile']
        model = USER


class AuthenticateForm(AuthenticationForm):
    username = forms.CharField(widget=forms.widgets.TextInput(
        attrs={'placeholder': 'Username', 'class': "form-control"}))
    password = forms.CharField(widget=forms.widgets.PasswordInput(
        attrs={'placeholder': 'Password', 'class': "form-control"}))

    def is_valid(self):
        form = super(AuthenticateForm, self).is_valid()
        for field, error in self.errors.items():
            if field != '__all__':
                self.fields[field].widget.attrs.update(
                    {'class': 'error', 'value': strip_tags(error)})
        return form


class UserEditForm(UserChangeForm):
    password = None
    first_name = forms.CharField(required=False,
                                 widget=forms.widgets.TextInput(
                                     attrs={'placeholder': 'First Name', 'class': "form-control"}))
    last_name = forms.CharField(required=False,
                                widget=forms.widgets.TextInput(
                                    attrs={'placeholder': 'Last Name', 'class': "form-control"}))
    mobile = forms.CharField(required=True,
                             widget=forms.widgets.TextInput(
                                 attrs={'placeholder': 'Mobile Phone', 'class': "form-control"}))

    def is_valid(self):
        form = super(UserEditForm, self).is_valid()
        for field, error in self.errors.items():
            if field != '__all_':
                self.fields[field].widget.attrs.update(
                    {'class': 'error', 'value': strip_tags(error)})
        return form

    class Meta:
        fields = ['first_name', 'last_name', 'mobile']
        model = USER

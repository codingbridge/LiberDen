from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm, PasswordChangeForm, PasswordResetForm
from django.utils.html import strip_tags
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator

phone_validator = RegexValidator(r"^(?:\+?86)?1(?:3\d{3}|5[^4\D]\d{2}|8\d{3}|7(?:[35678]\d{2}|4(?:0\d|1[0-2]|9\d))|9[189]\d{2}|66\d{2})\d{6}$", 
                                "phone number is not valid.")
User = get_user_model()


class UserCreateForm(UserCreationForm):
    username = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Username','class': "form-control"}))
    password1 = forms.CharField(required=True, widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Password','class': "form-control"}))
    password2 = forms.CharField(required=True,
                                widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Password Confirmation','class': "form-control"}))
    mobile = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'mobile phone','class': "form-control"}),
                             validators=[])

    def is_valid(self):
        form = super(UserCreateForm, self).is_valid()
        for f, error in self.errors.items():
            if f != '__all_':
                self.fields[f].widget.attrs.update({'class': 'error', 'value': strip_tags(error)})
        return form

    def save(self):
        user = super(UserCreateForm, self).save()
        return user

    class Meta:
        fields = ['username', 'password1', 'password2', 'mobile', 'first_name', 'last_name']
        model = User


class AuthenticateForm(AuthenticationForm):
    username = forms.CharField(widget=forms.widgets.TextInput(attrs={'placeholder': 'Username','class': "form-control"}))
    password = forms.CharField(widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Password','class': "form-control"}))

    def is_valid(self):
        form = super(AuthenticateForm, self).is_valid()
        for f, error in self.errors.items():
            if f != '__all__':
                self.fields[f].widget.attrs.update({'class': 'error', 'value': strip_tags(error)})
        return form


class UserChangeForm(UserChangeForm):
    first_name = forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={'placeholder': 'First Name','class': "form-control"}))
    last_name = forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={'placeholder': 'Last Name','class': "form-control"}))
    mobile = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Mobile Phone','class': "form-control"}))

    def is_valid(self):
        form = super(UserChangeForm, self).is_valid()
        for f, error in self.errors.items():
            if f != '__all_':
                self.fields[f].widget.attrs.update({'class': 'error', 'value': strip_tags(error)})
        return form

    def save(self):
        user = super(UserChangeForm, self).save()
        return user


    class Meta:
        fields = ['first_name', 'last_name', 'mobile']
        model = User


class PasswordChangeForm(PasswordChangeForm):
    pass


class PasswordResetForm(PasswordResetForm):
    pass
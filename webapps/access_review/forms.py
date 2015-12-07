from models import *

__author__ = 'liukaiyu'
from django import forms
from django.core.validators import validate_email, RegexValidator


class ManagerRegistrationForm(forms.Form):

    username = forms.CharField(max_length=30)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.CharField(max_length=50,validators = [validate_email])
    password1 = forms.CharField(max_length = 200,
                                 label='Password',
                                 widget = forms.PasswordInput())
    password2 = forms.CharField(max_length = 200,
                                 label='Confirm password',
                                 widget = forms.PasswordInput())



class AuditorRegistrationForm(forms.Form):

    username = forms.CharField(max_length=30)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.CharField(max_length=50,validators = [validate_email])
    password1 = forms.CharField(max_length = 200,
                                 label='Password',
                                 widget = forms.PasswordInput())
    password2 = forms.CharField(max_length = 200,
                                 label='Confirm password',
                                 widget = forms.PasswordInput())

class AdminRegistrationForm(forms.Form):

    username = forms.CharField(max_length=30)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.CharField(max_length=50,validators = [validate_email])
    password1 = forms.CharField(max_length = 200,
                                 label='Password',
                                 widget = forms.PasswordInput())
    password2 = forms.CharField(max_length = 200,
                                 label='Confirm password',
                                 widget = forms.PasswordInput())


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length = 200,
                                 label='Password',
                                 widget = forms.PasswordInput())

class PermissionForm(forms.ModelForm):
    read = "Read"
    read_write = "Read-write"
    choices = (
        (read, u'Read'),
        (read_write, u'Read and Write'),
    )

    class Meta:
        model = App_Permission
        fields = (
            'status',
        )

    status = forms.ChoiceField(choices = choices,  widget=forms.Select(), required=True)

    def clean(self):
        cleaned_data = super(PermissionForm, self).clean()
        status = cleaned_data.get('status')

        if status == None:
            raise forms.ValidationError('You should have status')
        return cleaned_data

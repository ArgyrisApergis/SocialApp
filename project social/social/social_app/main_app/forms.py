from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm

class CommentForm(forms.ModelForm):
    body = forms.CharField(required=True, 
    widget=forms.widgets.Textarea (attrs={"placeholder": "Comment something...","class": "textarea is-success is-medium",}),label="",)

    class Meta:
        model = Comments
        exclude = ("user", )

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
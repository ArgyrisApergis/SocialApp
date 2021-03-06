from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm,UsernameField

class CommentForm(forms.ModelForm):
    body = forms.CharField(required=True, 
    widget=forms.widgets.Textarea (attrs={"placeholder": "Comment something...","class": "textarea is-success is-small",}),label="",)

    class Meta:
        model = Comments
        exclude = ("user", )

class LoginForm(forms.Form):
    username = UsernameField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label=("Password"), strip=False, widget=forms.PasswordInput(attrs={'class':'form-control'}))


class RegisterForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder':'Password'}))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password'}))
    
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        widgets = {'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Username'})}


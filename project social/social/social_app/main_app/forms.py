from django import forms
from .models import *

class CommentForm(forms.ModelForm):
    body = forms.CharField(required=True, 
    widget=forms.widgets.Textarea (attrs={"placeholder": "Comment something...","class": "textarea is-success is-medium",}),label="",)

    class Meta:
        model = Comments
        exclude = ("user", )
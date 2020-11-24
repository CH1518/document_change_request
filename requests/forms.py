from django import forms
# from simple_forms.apps.core.models import Person
from django.forms import ModelForm
from .models import Comment
from django.db import models

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
 

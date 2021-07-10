from django import forms
from django.forms import ModelForm
from .models import Comment


class EditCommentForm(ModelForm):
    """
    Comment form. Used with edit_comment view and template
    """
    class Meta:
        model = Comment
        fields = ['body']

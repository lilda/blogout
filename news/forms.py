from django import forms
from .models import News

class NewsPost(forms.ModelForm):
    class Meta:
        model=News
        fields=["title", "content", "photo"]
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import Comment, Critic, Act, Community


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password',)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'text',)


class CriticForm(forms.ModelForm):
    class Meta:
        model = Critic
        fields = ('act', 'title', 'text',)


class ActForm(forms.ModelForm):
    class Meta:
        model = Act
        fields = ('name', 'community', 'author', 'director', 'preview', 'image',)


class ComForm(forms.ModelForm):
    class Meta:
        model = Community
        fields = ('name',)


class TempUserForm(forms.Form):
    email = forms.CharField(label='Email', max_length=50)

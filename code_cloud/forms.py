from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Problem, Tags, Share

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class ProblemForm(ModelForm):
    class Meta:
        model = Problem
        fields = ('name', 'online_judge', 'difficulty', 'access', 'docfile')

class TagForm(ModelForm):
    class Meta:
        model = Tags
        fields = ('tag', 'problem')

class ShareForm(ModelForm):
    class Meta:
        model = Share
        fields = ('problem', 'share_user')

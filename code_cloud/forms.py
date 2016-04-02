from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Problem, Tags

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

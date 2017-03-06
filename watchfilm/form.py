#coding=utf-8
from django import forms
from models import UserProfile, User, UserAddList


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password', 'email')


class UserProfileForm(forms.ModelForm):
    picture = forms.ImageField(required=False)

    class Meta:
        model = UserProfile
        fields = ('picture',)


class UserAddListForm(forms.ModelForm):
    name = forms.CharField(max_length=30, help_text='影视名称')
    describe = forms.CharField(required=False, help_text='影视描述或其他')
    url = forms.URLField(help_text='影视地址')

    class Meta:
        model = UserAddList
        fields = ('name', 'describe', 'url')
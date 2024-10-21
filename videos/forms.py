from django import forms
from .models import Video
from .models import UserProfile

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'description', 'file']
        labels={
            'title':'标题',
            'description':'简介',
            'file':'文件',
        }

class AvatarUploadForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar']
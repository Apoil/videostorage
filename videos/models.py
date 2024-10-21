from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils.text import slugify

def video_upload_path(instance,filename):
    title_file=instance.title
    return f'upload/videos/{title_file}/{filename}'  

def cover_upload_path(instance, filename):  
    title_slug = slugify(instance.title)  
    return f'upload/covers/{title_slug}/{filename}'  

def user_name(instance, filename):  
    title_slug = slugify(instance.username)  
    return f'images/avatars/{title_slug}/'  

class Video(models.Model):
    title=models.CharField(max_length=255)
    description=models.TextField()
    file=models.FileField(upload_to=video_upload_path)
    cover = models.ImageField(upload_to=cover_upload_path, blank=True, null=True)
    uploaded_at=models.DateTimeField(auto_now_add=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='images/avatars/', null=True, blank=True)
    def __str__(self):
        return self.user.username
    

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('upload/', views.upload_video, name='upload_video'),
    path('user/<int:user_id>/', views.user_detail, name='user_detail'),
    path('upload-avatar/', views.upload_avatar, name='upload_avatar'),


]

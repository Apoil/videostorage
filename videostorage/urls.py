from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include
from videos import views as video_views

urlpatterns = [
    path('admin/', admin.site.urls),
     path('login/', video_views.login_view, name='login'),
     path('', video_views.home, name='home'),  # 根URL指向主页视图
    path('videos/',include('videos.urls')),
    path('videos/', video_views.video_list, name='video_list'),  
    path('videos/<int:video_id>/play/', video_views.play_video, name='play_video'), 
    path('video/stream/<int:video_id>/', video_views.stream_video, name='stream_video'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

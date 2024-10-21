import mimetypes
import os
import re
from wsgiref.util import FileWrapper
from django.http import HttpResponse, StreamingHttpResponse, FileResponse, Http404
from django.shortcuts import redirect, render,get_object_or_404
from django.contrib.auth import login,authenticate
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from .models import Video
from .models import UserProfile
from .forms import AvatarUploadForm
from django.contrib.auth import logout
from .forms import VideoForm
from .utils import save_video_first_frame
from django.contrib.auth.models import User
import psutil
import json



@login_required(login_url='/login/')
def home(request):
    videos = Video.objects.all()  
    #context = {'videos': videos}
    if 'logout' in request.POST:
        logout(request)
        return redirect('/login/')  # 登出后重定向到登录页面
    disk_usage = None
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.filter(user=request.user).first()



        # 获取磁盘使用情况（这里以根目录'/'为例）  
        try:  
            disk_usage = psutil.disk_usage('/')  
            total = disk_usage.total / (1024.0 ** 3)  # 转换为 GB  
            used = disk_usage.used / (1024.0 ** 3)    # 转换为 GB  
            free = disk_usage.free / (1024.0 ** 3)    # 转换为 GB  
            # 你可以将这三个值分开传递给模板，或者将它们组合成一个字典  
            disk_info = {'total': total, 'used': used, 'free': free}  
        except Exception as e:  
            # 处理可能出现的异常，例如权限问题或磁盘不可访问  
            disk_info = {'total': 0, 'used': 0, 'free': 0, 'error': str(e)}  
    else:
        user_profile = None
        disk_info = None
    return render(request, 'home.html', {                                         
        'user_profile': user_profile,
        'user': request.user,
        'disk_info': disk_info,
        'videos': videos
    })

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # 保存用户并获取用户实例
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')  # 从表单中获取密码1

            
            # 认证用户
            user = authenticate(username=username, password=password)
            if user is not None:
                # 用户认证成功，登录
                login(request, user)
                return redirect('home')
            else:
                # 用户认证失败处理
                return render(request, 'signup.html', {'form': form, 'error': 'Authentication failed'})
    else:
        form = UserCreationForm()
    
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method=='POST':
        form=AuthenticationForm(data=request.POST)
        if form.is_valid():
            user=form.get_user()
            login(request,user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': '用户名或密码错误'})
    else:
        form=AuthenticationForm()

    return render(request,'login.html',{'form':form})

@login_required
def upload_video(request):
    if request.method=='POST':
        form=VideoForm(request.POST,request.FILES)
        if form.is_valid():
            video=form.save(commit=False)
            video.user=request.user
            if request.FILES.get('file'):
                cover_image = save_video_first_frame(request.FILES['file'])
                if cover_image:
                    video.cover.save(cover_image.name, cover_image)

            video.save()
            return redirect('home')
    
    else:
        form=VideoForm()
    return render(request,'uplaod_video.html',{'form':form})

def user_detail(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user_profile, created = UserProfile.objects.get_or_create(user=user)
    return render(request, 'user_detail.html', {'user': user, 'user_profile': user_profile})


@login_required
def upload_avatar(request):
    if request.method == 'POST':
        form = AvatarUploadForm(request.POST, request.FILES, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            return redirect('user_detail', user_id=request.user.id)
    else:
        form = AvatarUploadForm(instance=request.user.userprofile)
    return render(request, 'upload_avatar.html', {'form': form})


def video_list(request):  
    # 获取所有视频（或根据需要进行过滤）  
    videos = Video.objects.all()  
    context = {'videos': videos}  
    return render(request, 'video_list.html', context)  

def play_video123(request, video_id):  
    # 根据video_id获取视频对象  
    video = Video.objects.get(id=video_id)  
    context = {'video': video}  
    return render(request, 'play_video.html', context)



# 渲染页面视图
def play_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    context = {'video': video}
    return render(request, 'play_video.html', context)


def file_iterator(file_name, chunk_size=8192, offset=0, length=None):
    """ 逐块读取文件，以便于流式响应 """
    with open(file_name, "rb") as f:
        f.seek(offset, os.SEEK_SET)  # 定位到指定的字节位置
        remaining = length
        while True:
            bytes_length = chunk_size if remaining is None else min(remaining, chunk_size)
            data = f.read(bytes_length)
            if not data:
                break
            if remaining:
                remaining -= len(data)
            yield data

def stream_video(request, video_id):
    # 根据视频ID获取视频对象
    video = get_object_or_404(Video, id=video_id)
    video_path = video.file.path  # 视频文件的路径

    if not os.path.exists(video_path):
        raise Http404("Video not found")

    # 获取文件大小和类型
    size = os.path.getsize(video_path)
    content_type, encoding = mimetypes.guess_type(video_path)
    content_type = content_type or 'application/octet-stream'

    # 处理 Range 请求头
    range_header = request.META.get('HTTP_RANGE', '').strip()
    range_re = re.compile(r'bytes\s*=\s*(\d+)\s*-\s*(\d*)', re.I)
    range_match = range_re.match(range_header)

    if range_match:
        first_byte, last_byte = range_match.groups()
        first_byte = int(first_byte) if first_byte else 0
        last_byte = int(last_byte) if last_byte else first_byte + 1024 * 1024 * 8  # 8MB per chunk

        if last_byte >= size:
            last_byte = size - 1

        length = last_byte - first_byte + 1
        response = StreamingHttpResponse(
            file_iterator(video_path, offset=first_byte, length=length),
            status=206,  # Partial content
            content_type=content_type
        )
        response['Content-Length'] = str(length)
        response['Content-Range'] = f'bytes {first_byte}-{last_byte}/{size}'
    else:
        # 如果没有 Range 请求头，返回整个视频文件
        response = StreamingHttpResponse(FileWrapper(open(video_path, 'rb')), content_type=content_type)
        response['Content-Length'] = str(size)

    response['Accept-Ranges'] = 'bytes'  # 告诉浏览器支持字节范围请求
    return response
from multiprocessing import context
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import auth
from django.contrib.auth.forms import AuthenticationForm
from cuapp.forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

# Create your views here.


def index(request):  # 회원정보를 의미함
    return render(request, 'index.html')


def signup(request):  # 회원가입을 의미함
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth.login(request, user)
            return redirect('login')
        else:
            return render(request, 'signup.html', {'form': form})
    else:
        form = CustomUserCreationForm()
        return render(request, 'signup.html', {'form': form})


def login(request):  # 로그인을 의미함
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)
            return redirect('write')
        else:
            return render(request, 'login.html', {'form': form})
    else:
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})


def logout(request):  # 로그아웃을 의미함
    auth.logout(request)
    return redirect('index')


def update_password(request):  # 비밀번호 수정을 의미함
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()  # 이때 로그아웃처리됨. session 정보 날라가고, 로그인정보도 사라짐
            # session 을 update 이렇게 해야 비밀번호를 바꾸더라도 로그아웃이 되지 않음
            update_session_auth_hash(request, user)
            return redirect('update_password')
    else:
        form = PasswordChangeForm(request.user)
    context = {
        'form': form,
    }
    return render(request, 'update_password.html', context)  # mypage.html로 이동


def mypage(request):
    return render(request, 'mypage.html')

#프로필 이미지 수정


def update_user(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(
            request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            image = request.user.user_image
            return render(request, 'mypage.html', {'image': image})
    else:
        form = CustomUserChangeForm(instance=request.user)
        image = request.user.user_image
        return render(request, 'update_user.html', {
            'form': form,
            'image': image})

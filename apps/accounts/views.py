from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard:home')
        else:
            messages.error(request, 'Username yoki parol noto\'g\'ri')
    return render(request, 'accounts/login.html')


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if password != password2:
            messages.error(request, 'Parollar mos kelmadi')
            return render(request, 'accounts/register.html')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Bu username band')
            return render(request, 'accounts/register.html')
        user = User.objects.create_user(
            username=username, email=email,
            first_name=first_name, last_name=last_name,
            password=password, role='student'
        )
        login(request, user)
        messages.success(request, 'Muvaffaqiyatli ro\'yxatdan o\'tdingiz!')
        return redirect('dashboard:home')
    return render(request, 'accounts/register.html')


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def profile_view(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.phone = request.POST.get('phone', user.phone)
        user.bio = request.POST.get('bio', user.bio)
        user.telegram = request.POST.get('telegram', user.telegram)
        if request.FILES.get('avatar'):
            user.avatar = request.FILES['avatar']
        user.save()
        messages.success(request, 'Profil yangilandi!')
        return redirect('accounts:profile')
    return render(request, 'accounts/profile.html', {'user': request.user})

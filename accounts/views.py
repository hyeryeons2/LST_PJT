from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm #, UserCreationForm, UserChangeForm
# 그냥 login 이라 하면 중복 
from django.contrib.auth import login as auth_login, logout as auth_logout, update_session_auth_hash 
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import CustomUserChangeForm, CustomUserCreationForm, CustomPasswordChangeForm, GuildForm
from .models import Guild, User


def index(request):
    users = User.objects.all()
    context = {'users': users}
    return render(request, 'accounts/index.html', context)

# request.user.username
def signup(request):
    # if request.user.is_authenticated:
    #     return redirect('accounts:index')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # return redirect('accounts:login')
            auth_login(request, user)
            return redirect('movies:index')
    else: # == 'GET'
        form = CustomUserCreationForm()
    context = {'form': form}
    return render(request, 'accounts/signup.html', context)


# session data 를 만드는 것 
def login(request):
    # if request.user.is_authenticated:
    #     return redirect('articles:index')
    if request.method == 'POST':
        # 얘만 request 가 들어간다 
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            next_page = request.GET.get('next')
            # GET 요청
            return redirect(next_page or 'movies:index')
    else:
        form = AuthenticationForm()
    context = {'form': form}
    return render(request, 'accounts/login.html', context)


def logout(request):
    auth_logout(request)
    return redirect('movies:intro')


@require_POST
def delete(request):
    if request.user.is_authenticated:
        request.user.delete()
    return redirect('movies:intro')


# 로그인이 된 상태라 id 값으로 판별할 필요가 없음 
@login_required
def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('movies:index')
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {'form': form}
    return render(request, 'accounts/update.html', context)


@login_required
def password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # 재로그인?
            # 비밀번호가 바뀌면 세션 정보가 일치하지 않게 되서 로그아웃됨 
            update_session_auth_hash(request, user)
            return redirect('movies:index')
    else:
        # 비밀번호 변경 form이 필요
        form = CustomPasswordChangeForm(request.user) 
    context = {'form': form}
    return render(request, 'accounts/password.html', context)


def liguild(request):
    guilds = Guild.objects.all()
    context = {'guilds': guilds}
    return render(request, 'accounts/liguild.html', context)


@login_required
def mkguild(request):
    if request.method == 'POST':
        form = GuildForm(request.POST) 
        if form.is_valid():
            guild = form.save(commit=False)
            # .master 로 해야 master 의 id 에 접근 가능 
            guild.master = request.user
            guild.level = 1 
            guild.save()
            request.user.group_id = guild.id
            request.user.save()
            return redirect('accounts:liguild')
    else:
        form = GuildForm()
    context = {'form': form}
    return render(request, 'accounts/mkguild.html', context)
    

def joinguild(request, guild_pk):
    guild = get_object_or_404(Guild, pk=guild_pk)
    request.user.group_id = guild_pk
    request.user.save()
    return redirect('accounts:liguild')


def leaveguild(request):
    request.user.group_id = None
    request.user.save()
    return redirect('accounts:liguild')

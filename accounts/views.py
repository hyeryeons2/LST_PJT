from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm #, UserCreationForm, UserChangeForm
# 그냥 login 이라 하면 중복 
from django.contrib.auth import login as auth_login, logout as auth_logout, update_session_auth_hash 
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import CustomUserChangeForm, CustomUserCreationForm


def index(request):
    return render(request, 'accounts/index.html')

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
            return redirect('accounts:index')
    else: # == 'GET'
        form = CustomUserCreationForm()
    context = {'form': form}
    return render(request, 'accounts/signup.html', context)

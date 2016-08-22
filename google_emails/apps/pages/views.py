from django.shortcuts import render
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.shortcuts import redirect


@login_required(login_url=reverse_lazy('pages:login'))
def index(request):
    return render(request, 'index.html')


def login_user(request):
    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return redirect('pages:login')





from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render


@login_required(login_url='/signin')
def home(request):
    return render(request, 'home.html')


def sign_in(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    return render(request, 'login.html')

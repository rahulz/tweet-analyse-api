import json

import pandas
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from utils.tweepy.helpers import TweePy


@login_required(login_url='/signin')
def home(request):
    return render(request, 'home.html')


def sign_in(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    return render(request, 'login.html')


@login_required
def trends(request):
    tp = TweePy(request.user)
    trends = tp.get_trends()
    df = pandas.DataFrame(trends[0]['trends'])

    return HttpResponse(df['name'].to_json(orient='values'))

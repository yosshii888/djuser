from django.shortcuts import render, redirect, reverse
from django.contrib.auth.models import User
from django.contrib.auth import logout, login
from django.http import HttpResponseRedirect
from django.db import IntegrityError
from django.conf import settings
from django.views.generic import View
from django.shortcuts import render, get_object_or_404
from .forms import SignUpForm, LogInForm


from django.views import View
from django.shortcuts import render

class IndexView(View):
    def get(self, request, *args, **kwargs):
        # ログインしているか確認
        if request.user.is_authenticated:
            # ユーザー名を取得
            username = request.user.username
        else:
            username = None

        return render(request, 'app/index.html', {'username': username})

class SignUpView(View):
    def get(self, request, *args, **kwargs):

        return render(request, "app/signup.html")

    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']            
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            password2 = form.cleaned_data['password2']

            if password == password2:
                try:
                    user = User.objects.create_user(name,email, password)
                    user.save()
                    return HttpResponseRedirect(reverse('login'))
                except IntegrityError:
                    return render(request, "app/signup.html", {'error': 'このユーザーはすでに登録されています'})
            else:
                return render(request, "app/signup.html", {'error': 'パスワードが再入力と一致しません'})
        else:
            return render(request, "app/signup.html", {'error': '入力内容をもう一度確認してください'})

from django.contrib.auth import authenticate, login

class LogInView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "app/login.html")

    def post(self, request, *args, **kwargs):
        form = LogInForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect("index")
            else:
                return render(request, "app/login.html", {'error': 'emailかパスワードが違います'})

class LogOutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("index")

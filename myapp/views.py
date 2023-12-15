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


from django.shortcuts import render
# PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteViewを追加
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.urls import reverse_lazy

class PasswordChange(LoginRequiredMixin, PasswordChangeView):
    """パスワード変更ビュー"""
    success_url = reverse_lazy('password_change_done')
    template_name = 'app/password_change.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # 継承元のメソッドCALL
        context["form_name"] = "password_change"
        return context


class PasswordChangeDone(LoginRequiredMixin,PasswordChangeDoneView):
    """パスワード変更しました"""
    template_name = 'app/password_change_done.html'

# --- ここから追加
class PasswordReset(PasswordResetView):
    """パスワード変更用URLの送付ページ"""
#    subject_template_name = 'app/mail_template/reset/subject.txt'
#    email_template_name = 'app/mail_template/reset/message.txt'
    template_name = 'app/password_reset.html'
    success_url = reverse_lazy('password_reset_done')


class PasswordResetDone(PasswordResetDoneView):
    """パスワード変更用URLを送りましたページ"""
    template_name = 'app/password_reset_done.html'


class PasswordResetConfirm(PasswordResetConfirmView):
    """新パスワード入力ページ"""
    success_url = reverse_lazy('password_reset_complete')
    template_name = 'app/password_reset_confirm.html'


class PasswordResetComplete(PasswordResetCompleteView):
    """新パスワード設定しましたページ"""
    template_name = 'app/password_reset_complete.html'

# --- ここまで
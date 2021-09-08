from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse


class LoginCustomView(LoginView):
    template_name = 'login.html'


class JoinCustomView(LoginView):
    template_name = 'join.html'

    def post(self, request, *args, **kwargs):
        try:
            user = User(username=request.POST.get('username'))
            user.set_password(request.POST.get('password'))
            user.save()
            return render(request, 'alert.html',
                          {'message': '회원가입 성공!',
                           'redirect_url': reverse('login')})
        except:
            return render(request, 'alert.html',
                          {'message': '회원가입 실패',
                           'redirect_url': reverse('join')})

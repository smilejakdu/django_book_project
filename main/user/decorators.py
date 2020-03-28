from django.shortcuts import redirect
from .models          import User


# login_required 데코레이터를 직접 작성해주었네요..
# 사실 django에는 login_required decorator가 이미 존재해서, 그..걸 써도 되지않을까 생각합니다..
def login_required(function):
    def wrap(request, *args, **kwargs):
        user = request.session.get('user')
        if user is None or not user:
            return redirect('/user/login')

        return function(request, *args, **kwargs)

    return wrap


# 해댕부분도 django의 login_required decorator가 이미 존재해서, 그..걸 써도 되지않을까 생각합니다..
def admin_required(function):
    def wrap(request, *args, **kwargs):
        user = request.session.get('user')
        if user is None or not user:
            return redirect('/user/login')

        user = User.objects.get(email=user)
        if user.level != 'admin':
            return redirect('/')

        return function(request, *args, **kwargs)

    return wrap

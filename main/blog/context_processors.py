from user.models import User


# base.html 같은 곳에서도 공통적으로 쓰고싶은 경우에 context_processor 를 이용해서 값을 전파시키면 된다
# 해당 옵션을 이용해서 render 함수 이전에 해당 함수가 호출이 됩니다. ㅇㅇ
def get_username(request):
   email = request.session.get('user')
   if email is not None:
      username = User.objects.get(email=email).email
   else:
      username = ''
   return {'email': username}

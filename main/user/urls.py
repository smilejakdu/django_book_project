from .           import views
from django.urls import path
from .views import LoginView , RegisterView , logout
urlpatterns = [
    path('logout/'   , views.logout, name='logout'),
    path('login/'    , LoginView.as_view(), name='login'),
    path('register/' , RegisterView.as_view(), name='register'),
]

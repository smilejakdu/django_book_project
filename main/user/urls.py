from .           import views
from django.urls import path
urlpatterns = [
    path('logout/'   , views.logout, name='logout'),
    path('login/'    , views.LoginView.as_view(), name='login'),
    path('register/' , views.RegisterView.as_view(), name='register'),
]

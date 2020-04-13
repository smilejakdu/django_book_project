from django.urls    import path, include

urlpatterns = [
    path('blog/'  , include('blog.urls')),
    path('user/'  , include('user.urls')),
]

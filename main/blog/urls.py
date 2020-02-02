from django.contrib import admin
from django.urls import path
from . import views

# URL 라우팅 추가.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('create/', views.post_create, name='create'),
    path('<int:pk>/', views.post_detail, name='detail'),
    path('<int:pk>/update/', views.post_update, name='update'),
    path('<int:pk>/delete/', views.post_delete, name='delete'),
    path('comment/<int:pk>/create/', views.comment_create, name='comment_create'),  # 댓글 작성 부분 URL 라우팅
    path('comment/<int:pk>/update/', views.comment_update, name='comment_update'),  # 댓글 수정 부분 URL 라우팅
    path('comment/<int:pk>/delete/', views.comment_delete, name='comment_delete'),  # 댓글 삭제 부분 URL 라우팅
    path('book_search/', views.book_search, name='book_search'),
    path('kyobo/', views.kyobo, name='kyobo')
]

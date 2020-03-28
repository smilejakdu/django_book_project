from django.contrib import admin
from .models        import Post, Book, Comment

# Register your models here.

admin.site.register(Post)
admin.site.register(Book)
admin.site.register(Comment)  # 여기에 작성한 Comment 모델을 등록해줌

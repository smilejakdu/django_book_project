from django.db import models


class Post(models.Model):
    title      = models.CharField(max_length=100, blank=True, null=True)
    author     = models.CharField(max_length=10, blank=True, null=True)
    date       = models.DateField(blank=True, null=True)
    content    = models.TextField(blank=True, null=True)
    writer     = models.TextField(max_length=255, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Meta 클래스를 재정의해서 옵션 설정가능.
    class Meta:
        app_label = 'blog'
        db_table  = 'post'


# 댓글 테이블
class Comment(models.Model):
    id               = models.AutoField(primary_key=True)
    writer           = models.TextField(max_length=255, blank=False, null=False)
    date             = models.DateField(blank=True, null=True)
    content          = models.TextField(blank=True, null=True)
    approved_comment = models.BooleanField(default=False)

    # Post의 Primary Key를 외래키로 지정해 놓는다.
    # 이런식으로, 특정 post 안의 댓글 모델을 구현한다.
    # 자세한 내용은 데이터베이스 1~2 정규화 내용 참조.
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')

    def approve(self):
        self.approved_comment = True
        self.save()

    class Meta:
        app_label = 'blog'  # 이런식으로, 해당 모델이 속한 앱을 명시해주어야 한다.
        db_table = 'comment'
        # managed = False # Managed 플래그는, 모델이 갱신되도, Database 테이블은 갱신이 안되게하는 옵션임. 유의바랍니다.


class Book(models.Model):
    num            = models.AutoField(primary_key=True)
    title          = models.CharField(max_length=100, blank=True, null=True)
    author         = models.CharField(max_length=100, blank=True, null=True)
    image          = models.CharField(max_length=250, blank=True, null=True)
    url            = models.CharField(max_length=250, blank=True, null=True)
    original_price = models.CharField(max_length=250, blank=True, null=True)
    sale_price     = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        app_label = 'blog'
        db_table  = 'book'

class Covid(models.Model):
    

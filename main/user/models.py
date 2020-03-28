from django.db import models


# Create your models here.

class User(models.Model):
    email    = models.EmailField(verbose_name='이메일' , unique = True)
    password = models.CharField(max_length=100, verbose_name='비밀번호')

    def __str__(self):
        return self.email

    class Meta:
        db_table            = 'user'
        verbose_name        = '사용자'
        verbose_name_plural = '사용자'

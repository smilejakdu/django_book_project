from django import forms
from .models import Post, Comment


# 포스트 내용을 받을 Form을 정의해줌.
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'author', 'content']

        widgets = {
            'title': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'width:200px; margin:20px;', 'placeholder': '제목을 입력하세요.'}
            ),
            'author': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'width:200px; margin:20px;', 'placeholder': '저자를 입력하세요.'}
            ),
            'content': forms.Textarea(
                attrs={'class': 'form-control', 'style': 'width:100%; height:50%; rows=3; margin:20px;',
                       'placeholder': '내용을 입력하세요.'}
            )
        }


# 댓글 내용을 받을 Form을 정의해줌.
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

        widgets = {
            'content': forms.Textarea(
                attrs={'class': 'form-control', 'style': 'width:90%; height:10%; rows=1; margin:1em;',
                       'placeholder': '내용을 입력하세요.'}
            )
        }


from django.urls    import path
from .views         import (home,
                            post_create,
                            post_detail,
                            post_update,
                            post_delete,
                            comment_create,
                            comment_delete,
                            book_search,
                            kyobo,
                            KyoboApiView,
                            CovidApiView,
                            BoardView,
                            BoardDetailView
                            )

urlpatterns = [
    path(''                         , home, name='home'),
    path('create/'                  , post_create, name='create'),
    path('<int:pk>/'                , post_detail, name='detail'),
    path('<int:pk>/update/'         , post_update, name='update'),
    path('<int:pk>/delete/'         , post_delete, name='delete'),
    path('comment/<int:pk>/create/' , comment_create, name='comment_create'),  # 댓글 작성 부분 URL 라우팅
    path('comment/<int:pk>/delete/' , comment_delete, name='comment_delete'),  # 댓글 삭제 부분 URL 라우팅
    path('book_search/'             , book_search, name='book_search'),
    path('kyobo/'                   , kyobo, name='kyobo'),
    path('book_api/'                , KyoboApiView.as_view(), name='book_api'),
    path('covid_api/'               , CovidApiView.as_view(), name= 'covid_api'),
    path('board'                    , BoardView.as_view()),
    path('board/<int:memo_id>'      , BoardDetailView.as_view()),
]

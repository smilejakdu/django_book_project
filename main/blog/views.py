import json
import urllib.request

from django.shortcuts      import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models      import Count, Q , Sum
from django.views          import View
from django.http           import HttpResponse, JsonResponse

from datetime              import *
from main.my_settings      import CLIENT_ID, CLIENT_SECRET
from user.decorators       import login_required
from .forms                import PostForm, CommentForm
from .models               import (Post,
                                   Book,
                                   Comment,
                                   Covid,
                                   KoreaCovid,
                                   Memo,
                                   Scheduler)

@login_required
def home(request):
    posts = Post.objects.all()  # 모든 Border 테이블의 모든 object들을 br에 저장하라
    # 검색 부분
    search = request.GET.get('search', '')  # GET request의 인자중에 b 값이 있으면 가져오고, 없으면 빈 문자열 넣기
    if search:  # search 에 값이 들어있으면 true
        posts = posts.filter(title__icontains=search)  # 의 title이 contains br의 title에 포함

    # 페이지 부분
    page = request.GET.get('page', 1)
    paginator = Paginator(posts, 5)  # Show 5 contacts per page

    # posts = paginator.get_page(page)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'index.html', {'posts': posts, 'search_data': search})


# 로그인 한 사람만 접근 가능하도록 login_required decorator 추가.
# 해당 함수는, 브라우저로 부터 제목, 저자, 내용을 받아서 포스트를 저장하는 함수이다. 
@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)

        # 로그인된 상태 및 form으로 제출한 내용을 체크해서 전부 유효한 경우, 게시물을 생성한다.
        if request.session['user'] is not None and form.is_valid():
            # form에서 바로 값을 추가하는것은 불가해서, 먼저 commit=False 옵션을 줘서 Save 한 뒤, 
            # post라는 변수로 값을 받아서 값을 써주고 다시 save해주어야 한다.
            post = form.save(commit=False)
            post.writer = request.session['user']
            post.date = datetime.today()  # DateTime 필드에 날짜를 저장할때는 아래와 같이 파이썬 내장 모듈인 datatime을 사용해서 날짜지정이 가능하다.
            post.save()
            return redirect('home')

    # POST 요청이 아닌 경우 단순히 Form 태그만 리턴한다.
    form = PostForm()

    return render(request, 'postcreate.html', {'form': form})


# 포스트 내용을 자세히 보여주는 페이지
@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # 아래와 같이, 포스트의 primary키를 이용해서, 해당 포스트에 속한 댓글들을 가져온다.
    comments = Comment.objects.filter(post=pk)
    comment_form = CommentForm()
    return render(request, 'postdetail.html', {'post': post, 'comments': comments, 'comment_form': comment_form})


@login_required
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # 게시글(포스트) 작성자가 아닌경우, 게시글(포스트) 수정을 불가능하게 함. 
    # 게시글 테이블에 저장된 작성자와 현재 세션의 작성자를 비교하는 방식으로 구현하였습니다.
    if request.session['user'] is not None and post.writer != request.session['user']:
        return redirect('home')

    # 갱신된 게시글(포스트)를 저장하는 부분입니다.
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('home')

    form = PostForm(instance=post)

    return render(request, 'postupdate.html', {'form': form})

@login_required
def post_delete(request, pk):
    post = Post.objects.get(pk=pk)

    # 게시글(포스트) 작성자가 아닌경우, 게시글(포스트) 삭제를 불가능하게 함. 
    # 게시글 테이블에 저장된 작성자와 현재 세션의 작성자를 비교하는 방식으로 구현하였습니다.
    if request.session['user'] is not None and post.writer == request.session['user']:
        post.delete()

    return redirect('home')

@login_required
def comment_create(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        # 댓글 내용을 받는 부분
        form = CommentForm(request.POST)
        if form.is_valid():
            # form에서 바로 값을 추가하는것은 불가해서, 먼저 commit=False 옵션을 줘서 Save 한 뒤,
            # comment라는 변수로 값을 받아서 값을 써주고 다시 save해주어야 한다.
            comment = form.save(commit=False)
            comment.writer = request.session['user']
            comment.post = post
            comment.date = datetime.today()  # DateTime 필드에 날짜를 저장할때는 아래와 같이 파이썬 내장 모듈인 datatime을 사용해서 날짜지정이 가능하다.
            comment.save()
            return redirect('detail', pk=comment.post.pk)

    form = CommentForm()
    return redirect('detail')


@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    # 댓글 작성자가 아닌경우, 댓글 삭제를 불가능하게 함. 
    # 댓글 테이블에 저장된 작성자와 현재 세션의 작성자를 비교하는 방식으로 구현
    if request.session['user'] is not None and comment.writer == request.session['user']:
        comment.delete()

    return redirect('detail', pk=comment.post.pk)


def book_search(request):
    if request.method == 'GET':

        input_data    = request.GET.get('input_search',None)
        encText       = urllib.parse.quote("{}".format(input_data))
        if input_data is None:
            # print('데이터가없습니다.')
            encText = urllib.parse.quote("Django")
        url = "https://openapi.naver.com/v1/search/book?query=" + encText  # json 결과
        book_api_request = urllib.request.Request(url)
        book_api_request.add_header("X-Naver-Client-Id"     , CLIENT_ID)
        book_api_request.add_header("X-Naver-Client-Secret" , CLIENT_SECRET)
        response = urllib.request.urlopen(book_api_request)
        if (response.getcode() == 200):
            response_body = response.read()
            items         = json.loads(response_body
                                       .decode('utf-8')).get('items')

            return render(request, 'book_search.html', {'items': items})

def kyobo(request):
    kyobo_book = Book.objects.all()

    return render(request, 'kyobo.html', {'kyobo_list': kyobo_book})


class KyoboApiView(View):
    def get(self, request):

        try:
            keyword = request.GET.get('keyword', None)
            if keyword:
                book_data    = Book.objects.filter(Q(author__icontains=keyword)).all().values()
                search_count = book_data.count()

                return JsonResponse(
                    {'data' : {
                        'book_count' : search_count,
                        'books'      : list(book_data)
                    }}, status=200)

            kyobo       = Book.objects.values()
            kyobo_count = Book.objects.count()

            return JsonResponse(
                {'data' : {
                    'book_count' : kyobo_count,
                    'books'      : list(kyobo)
                }}, status=200)

        except Book.DoesNotExist:
            return JsonResponse({'message': 'Not found'}, status=400)

        except TypeError:
            return JsonResponse({'message': 'error'}, status=400)

class CovidApiView(View):
    def get(self, request):
        try:
            query = request.GET.get('keyword',None) # 코로나 데이터 검색 
            if query:
                world_data           = Covid.objects.filter(Q(area__icontains=query) | Q(country__icontains=query)).all()
                korea_data          = KoreaCovid.objects.filter(Q(area__icontains=query)).all()
                world_patient_count = world_data.count()
                korea_patient_count = korea_data.count()

                data = {
                    'korea_count' : korea_patient_count,
                    'world_count' : world_patient_count,
                    'world_data'  : [{
                            'id'      : world.id,
                            'area'    : world.area,
                            'country' : world.country,
                            'patient' : world.patient,
                            'dead'    : world.dead,
                    } for world in world_data],
                    'korea_data' : [{
                            'id'      : korea.id,
                            'area'    : korea.area,
                            'patient' : korea.patient,
                    } for korea in korea_data],
                }

                return JsonResponse({"data" :data},status=200)

            country_covid     = Covid.objects.values()
            korea_covid       = KoreaCovid.objects.values()
            korea_covid_count = KoreaCovid.objects.all().aggregate(Sum('patient'))

            return JsonResponse({'data' : {
                                    'korea_covid_count' : korea_covid_count,
                                    'korea_covid'       : list(korea_covid),
                                    'country_covid'     : list(country_covid),
                                }}, status=200)

        except Covid.DoesNotExist:
            return JsonResponse({'message': 'Not found'}, status=400)

        except TypeError:
            return JsonResponse({'message': 'error'}, status=400)

class BoardView(View):
    def post(self , request):
        data    = json.loads(request.body)
        title   = data.get('title' , None)
        content = data.get('content' , None)
        try:
            if title and content:
                Memo(
                    title   = title,
                    content = content
                ).save()

                return HttpResponse(status=200)

        except TypeError:
            return HttpResponse(status=400)

        except Exception as  e:
            return JsonResponse({"ERROR" : e},status=400)

    def get(self , request):
        memo = Memo.objects.values()
        return JsonResponse({"data":list(memo)} , status=200)


class BoardDetailView(View):
    def post(self , request , memo_id):
        data      = json.loads(request.body)
        title     = data.get('title'   , None)
        content   = data.get('content' , None)
        memo_data = Memo.objects.get(id = memo_id)

        try :
            if title and content:
                memo_data.title   = title
                memo_data.content = content
                memo_data.save()

                return HttpResponse(status=200)

        except :
            return JsonResponse({"MESSAGE" : "ERROR"} , status=400)

    def delete(self , request , memo_id):
        memo_data = Memo.objects.get(id = memo_id)
        try :
            if memo_data.id:
                memo_data.delete()
                return HttpResponse(status=200)

        except ValueError:
            return HttpResponse(status=400)

        except Exception as e :
            return JsonResponse({"ERROR":e},status=400)


class SchedulerViewApi(View):
    def post(self , request):
        try:
            data       = json.loads(request.body)
            start_date = data.get('start_date' , None)
            end_date   = data.get('end_date'   , None)
            text       = data.get('text'       , None)

            if start_date and end_date and text:
                Scheduler(
                    start_date = start_date,
                    end_date   = end_date,
                    text       = text,
                ).save()

            return HttpResponse(status=200)

        except TypeError:
            return JsonResponse({"ERROR": "TYPE_ERROR"}, status=400)

        except Exception as e :
            return JsonResponse({"ERROR":e},status=400)

    def get(self , request):
        scheduler = Scheduler.objects.values()
        return JsonResponse({"data" : list(scheduler)} , status=200)

class SchedulerViewDetailApi(View):
    def post(self , request ,scheduler_id):
        try :
            data          = json.loads(request.body)
            start_date    = data.get('start_date' , None)
            end_date      = data.get('end_date'   , None)
            text          = data.get('text'       , None)
            schedule_data = Scheduler.objects.get(id=scheduler_id)

            if start_date and end_date and text:
                schedule_data.start_date = start_date
                schedule_data.end_date   = end_date
                schedule_data.text       = text
                schedule_data.save()

                return HttpResponse(status=200)

        except TypeError:
            return JsonResponse({"MESSAGE" : "TYPE_ERROR"} , status=400)

        except Exception as e:
            return JsonResponse({"ERROR":e},status=400)

    def delete(self , request ,scheduler_id):
        schedule_data = Scheduler.objects.get(id = scheduler_id)
        try :
            if schedule_data.id:
                schedule_data.delete()
                return HttpResponse(status=200)

        except Scheduler.DoesNotExist:
            return HttpResponse(status=400)


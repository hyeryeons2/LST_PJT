from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Recommendation, Movie, Review
from .forms import MovieForm, ReviewForm, RecommendationForm
from decouple import config
import requests
import bs4
from pprint import pprint


def intro(request):
    return render(request, 'movies/intro.html')


def index(request):
    movies = Movie.objects.all()
    context = {'movies': movies}
    return render(request, 'movies/index.html', context)


@login_required
def movielevellist(request):
    # 운영자면 모든 영화가 나옵니다
    if request.user.is_staff:
        movies = Movie.objects.all()
    else: 
        level = request.user.level 
        movies = Movie.objects.filter(level=level)
    context = {'movies': movies}
    return render(request, 'movies/movielevellist.html', context)


@require_GET
def detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    reviews = movie.reviews.all()
    form = ReviewForm()
    context = {
        'movie': movie,
        'reviews': reviews,
        'form': form,        
    }
    return render(request, 'movies/detail.html', context)


@login_required
def like(request, movie_pk):
    user = request.user
    movie = get_object_or_404(Movie, pk=movie_pk)
    if movie.liked_users.filter(pk=user.pk).exists():
        user.liked_movies.remove(movie)
        liked = False 
    else:
        user.liked_movies.add(movie)
        liked = True
    if len(user.liked_movies.all()) == 0:
        user.level = 1
    elif len(user.liked_movies.all()) == 1:
        user.level = 2
    else:
        user.level = 3
    user.save()
    context = {
        'liked': liked, 
        'count': movie.liked_users.count()
    }
    return redirect('movies:detail', movie_pk)
    # return JsonResponse(context)


@require_POST
def reviews(request, movie_pk):
    if request.user.is_authenticated:
        movie = get_object_or_404(Movie, pk=movie_pk)
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie_id = movie_pk
            review.user = request.user
            review.save()
    return redirect('movies:detail', movie_pk)


@login_required
def reviewupdate(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    movie_pk = review.movie_id
    movie = get_object_or_404(Movie, pk=movie_pk)
    reviews = movie.reviews.all()
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            form = ReviewForm()
            context = {
                'movie': movie,
                'reviews': reviews,
                'form': form,        
            }
    else: 
        form = ReviewForm()
        updateform = ReviewForm(instance=review)
        context = {
            'movie': movie,
            'reviews': reviews,
            'form': form,   
            'updateform': updateform, 
            'review_pk': review_pk, 
        }
    return render(request, 'movies/detail.html', context)


@require_POST
def reviewdelete(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    movie_pk = review.movie_id
    if review.user == request.user:
        review.delete()
    return redirect('movies:detail', movie_pk)


# 혹시 값이 이상하면 수동으로 하세요
@login_required
def addmovie(request):
    form =  MovieForm()
    if request.method == 'POST':
        movie = Movie()

        search = request.POST.get('movie')
        if not request.POST.get('listNM'):
            listnumber = 0
        else:
            listnumber = int(request.POST.get('listNM'))
        key = config('API_KEY')
        base_url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json'
        api_url = f'{base_url}?key={key}&movieNm={search}'
        response = requests.get(api_url)
        data = response.json()

        # number 바꾸면서 하는 중
        movieCd = data['movieListResult']['movieList'][listnumber]['movieCd']
        nation = data['movieListResult']['movieList'][listnumber]['repNationNm']
        movie.nation = nation

        base_url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json'
        api_url = f'{base_url}?key={key}&movieCd={movieCd}'
        response = requests.get(api_url)
        data = response.json()

        title = data['movieInfoResult']['movieInfo']['movieNm']
        movie.title = title
        title_en = data['movieInfoResult']['movieInfo']['movieNmEn']
        movie.title_en = title_en
        searchtitle = title_en.title()
        running_time = data['movieInfoResult']['movieInfo']['showTm']
        movie.running_time = running_time
        # index error 처리됨
        if data['movieInfoResult']['movieInfo']['audits'] == []:
            movie.watch_grade = '관람등급 알수없음'
        else:
            watch_grade = data['movieInfoResult']['movieInfo']['audits'][0]['watchGradeNm']
            movie.watch_grade = watch_grade
        genres = ''
        genre_list = data['movieInfoResult']['movieInfo']['genres']
        for genre in genre_list:
            genres += genre['genreNm'] + '|' 
        movie.genres = genres[:-1]
        openDt = data['movieInfoResult']['movieInfo']['openDt']
        movie.open_dt = openDt

        BASE_URL = 'https://openapi.naver.com/v1/search/movie.json'
        CLIENT_ID = config('CLIENT_ID')
        CLIENT_SECRET = config('CLIENT_SECRET')
        HEADER = {
            'X-Naver-Client-Id': CLIENT_ID,
            'X-Naver-Client-Secret': CLIENT_SECRET,
        }  
        API_URL = f'{BASE_URL}?query={search}'
        response = requests.get(API_URL, headers=HEADER).json()

        # 영어 제목으로 영진위 API 의 검색 결과와 네이버 API 의 검색 결과 연결 
        items = response['items']
        for item in items:
            if item['subtitle'].title() == searchtitle:
                directors = item['director']
                movie.directors = directors[:-1]
                actors = item['actor'] 
                movie.actors = actors[:-1]
                # 썸네일 가져오기
                # poster_url = item['image']
                # movie.poster_url = poster_url

                story_URL  = item['link']
                response = requests.get(story_URL)
                html = response.text
                soup = bs4.BeautifulSoup(html, 'html.parser')
                # 태그는 알아서 처리됨 
                description = soup.find('p', class_='con_tx').get_text()
                movie.description = description
                # 고화질 파일 가져오기 
                movie.poster_url = soup.select('div.poster > a > img')[0]['src'][:-15]
 
        url = 'https://www.googleapis.com/youtube/v3/search'
        params = {
            'key': config('YOUTUBE_API_KEY'),
            'part': 'snippet',
            'type': 'video',
            'maxResults': '1',
            'q': f'{search}' + '예고편',
        }
        response = requests.get(url, params)
        response_dict = response.json()
        link = response_dict['items'][0]['id']['videoId']
        preview_link = f'https://www.youtube.com/embed/{link}'
        movie.preview_link = preview_link

        params = {
            'key': config('YOUTUBE_API_KEY'),
            'part': 'snippet',
            'type': 'video',
            'maxResults': '1',
            'q': f'{search}' + '리뷰',
        }
        response = requests.get(url, params)
        response_dict = response.json()
        link = response_dict['items'][0]['id']['videoId']
        review_link = f'https://www.youtube.com/embed/{link}'
        movie.review_link = review_link
        if request.POST.get('recommend_id'):
            movie.recommendation = get_object_or_404(Recommendation, pk=request.POST.get('recommend_id'))
            movie.recommendation.finish = True 
            movie.recommendation.save()
        form = MovieForm(instance=movie)
    
    context = {'form': form}
    return render(request, 'movies/addmovie.html', context) 
    

@require_POST
def savemovie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('movies:index')
        context = {'form': form}
        return render(request, 'movies/addmovie.html', context)


# 영화 수정 삭제용
# def updatemovie(request, movie_pk):
#     pass


# def deletemovie(request, movie_pk):
#     pass


@login_required
def recommendation(request):
    if request.method == 'POST':
        form = RecommendationForm(request.POST)
        if form.is_valid():
            recommend = form.save(commit=False)
            recommend.recommend_user = request.user
            recommend.save()
            return redirect('movies:index')
    form = RecommendationForm()
    context = {'form': form}
    return render(request, 'movies/recommendation.html', context)


@login_required
def recommendlist(request):
    recommends = Recommendation.objects.all()
    context = {'recommends': recommends}
    return render(request, 'movies/recommendlist.html', context)

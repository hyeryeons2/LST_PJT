from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Recommendation, Movie, Review
from .forms import MovieForm
import requests
from decouple import config
from pprint import pprint
import bs4


def intro(request):
    return render(request, 'movies/intro.html')


def index(request):
    return render(request, 'movies/index.html')


def addmovie(request):
    form =  MovieForm()
    if request.method == 'POST':
        movie = Movie()

        search = request.POST.get('movie')
        key = config('API_KEY')
        base_url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json'
        api_url = f'{base_url}?key={key}&movieNm={search}'
        response = requests.get(api_url)
        data = response.json()

        # number 바꾸면서 할 예정 
        movieCd = data['movieListResult']['movieList'][0]['movieCd']
        nation = data['movieListResult']['movieList'][0]['repNationNm']
        movie.nation = nation

        base_url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json'
        api_url = f'{base_url}?key={key}&movieCd={movieCd}'
        response = requests.get(api_url)
        data = response.json()

        title = data['movieInfoResult']['movieInfo']['movieNm']
        movie.title = title
        title_en = data['movieInfoResult']['movieInfo']['movieNmEn']
        movie.title_en = title_en
        running_time = data['movieInfoResult']['movieInfo']['showTm']
        movie.running_time = running_time
        # index error 가능
        watch_grade = data['movieInfoResult']['movieInfo']['audits'][0]['watchGradeNm']
        movie.watch_grade = watch_grade
        genres = ''
        genre_list = data['movieInfoResult']['movieInfo']['genres']
        for genre in genre_list:
            genres += genre['genreNm'] + '|' 
        movie.genres = genres
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

        # number 같이 바꿀지 따로 바꿀지 생각해야됨 
        directors = response['items'][0]['director']
        movie.directors = directors
        actors = response['items'][0]['actor']
        movie.actors = actors
        poster_url = response['items'][0]['image']
        movie.poster_url = poster_url

        story_URL  = response['items'][0]['link']
        response = requests.get(story_URL)
        html = response.text
        soup = bs4.BeautifulSoup(html, 'html.parser')
        # 태그는 알아서 처리됨 
        description = soup.find('p', class_='con_tx').get_text()
        movie.description = description
 
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
        form = MovieForm(instance=movie)
    context = {'form': form}
    return render(request, 'movies/addmovie.html', context) 
    

def savemovie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('movies:index')
    return render(request, 'movies/addmovie.html', context)

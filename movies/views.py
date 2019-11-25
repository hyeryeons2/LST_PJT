from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Recommendation, Movie, Review
from .forms import MovieForm
import requests
from decouple import config
from pprint import pprint


def intro(request):
    return render(request, 'movies/intro.html')


def index(request):
    return render(request, 'movies/index.html')


def addmovie(request):
    if request.method == 'POST':
        search = request.POST.get('movie')
        key = config('API_KEY')
        base_url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json'
        api_url = f'{base_url}?key={key}&movieNm={search}'
        response = requests.get(api_url)
        data = response.json()

        # number 바꾸면서 할 예정 
        movieCd = data['movieListResult']['movieList'][0]['movieCd']
        nation = data['movieListResult']['movieList'][0]['repNationNm']

        base_url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json'
        api_url = f'{base_url}?key={key}&movieCd={movieCd}'
        response = requests.get(api_url)
        data = response.json()

        title = data['movieInfoResult']['movieInfo']['movieNm']
        title_en = data['movieInfoResult']['movieInfo']['movieNmEn']
        running_time = data['movieInfoResult']['movieInfo']['showTm']
        watch_grade = data['movieInfoResult']['movieInfo']['audits'][0]['watchGradeNm']
        genres = ''
        genre_list = data['movieInfoResult']['movieInfo']['genres']
        for genre in genre_list:
            genres += genre['genreNm'] + '|' 
        openDt = data['movieInfoResult']['movieInfo']['openDt']

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
        actors = response['items'][0]['actor']
        poster_url = response['items'][0]['image']

    # else: 
        # count = 0 
    form =  MovieForm()
    context = {'form': form}
    return render(request, 'movies/addmovie.html', context) 
    
# LST_PJT(영화추천사이트 제작)

## 0. Intro(하려고 하는 것, 개요)



## 1. django 환경설정 및 Setting



## 2. DB 모델링

- djangofield 수정

 https://stackoverflow.com/questions/24344981/how-to-change-help-text-of-a-django-form-field 


### 2.1 회원가입 MODELS.PY VALIDATION MESSAGE 수정

- [참고]
   https://github.com/django/django/blob/master/django/contrib/auth/forms.py#L77 

#### # Blank true, null true

-  model 오류나면 상위로 폴더 옮기면 됨(usermodel에서 user, group 할 때,  group 클래스를 상위로 옮김)



#### # ADMIN 등록(accounts, movies)



### accounts.models

#### class Guild

- 사용자들이 가입할 수 있는 Guild 모델 생성
- Guild 모델의 변수로 name, level, created_at 추가 
- master 는 Guild 를 생성하는 유저를 ForeignKey 로 받음 
- master 가 사라져도 guild instance 가 사라지지 않드로 on_delete 옵션을 SET_NULL 로 설정

#### class User

- User 모델을 커스텀하기 위해 AbstrctUser 를 상속하는 User 모델 생성
- User 모델의 변수로 nickname, age, level  추가
- followers 는 User 모델간 M:M 모델로 추가 
- Guild 모델로부터 group_id 를 ForeignKey 로 받음 
- group 이 사라져도 user 가 사라지지 않드로 on_delete 옵션을 SET_NULL 로 설정

```python
# accounts.models

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class Guild(models.Model):
    name = models.CharField(max_length=40)
    level = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    master = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)


class User(AbstractUser):
    nickname = models.CharField(max_length=20)
    age = models.IntegerField(blank=True, null=True)
    followers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='followings' 
    )
    group = models.ForeignKey(Guild, related_name='member', on_delete=models.SET_NULL, blank=True, null=True)
    level = models.IntegerField(default=1)
```



### accounts.forms

#### class CustomUserCreationForm



### movies.models

#### class Recommendation

- 사용자의 영화 등록 요청을 기록하기 위한 모델 
- Recommendation 모델의 변수로 title(영화 제목), content(요청 내용), created_at 추가 
- 등록한 유저의 정보를 저장하기 위해 recommend_user 에 user_id 를 ForeignKey 로 받음 
- finish 는 False 를 default 로 하고 영화가 등록되었을 때 True 로 바꿔줌 
- user 가 사라져도 recommendation instance 가 사라지지 않드로 on_delete 옵션을 SET_NULL 로 설정

#### class Movie

- 영화의 정보를 기록하기 위한 모델 
- Movie 모델에 수집해서 사용할 정보들을 필드로 정의
- 영화에 '좋아요' 를 한 유저들을 기록하기 위해 liked_users 를 M:M 필드로 생성 
- 영화 등록 요청을 기록하기 위해 recommendation 필드를 Recommendation 모델과 연결 
- recommendation 이 사라져도 movie instance 가 사라지지 않드로 on_delete 옵션을 SET_NULL 로 설정 

#### class Review

- 영화의 리뷰를 기록하기 위한 모델 
- Review 모델의 변수로 content, score, created_at 추가 
- 리뷰를 작성한 사용자를 기록하기 위해 User 모델의 ForeignKey 를 받아옴  
- 리뷰가 작성된 영화를 기록하기 위해 Movie 모델의 ForeignKey 를 받아옴 

```python
# movies.models

from django.db import models
from django.conf import settings


class Recommendation(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    recommend_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    finish = models.BooleanField(default=False)


class Movie(models.Model):
    title = models.CharField(max_length=50)
    title_en = models.CharField(max_length=100)
    poster_url = models.CharField(max_length=140)
    description = models.TextField()
    running_time = models.CharField(max_length=30)
    directors = models.CharField(max_length=100)
    actors = models.CharField(max_length=100)
    nation = models.CharField(max_length=50, blank=True, null=True)
    watch_grade = models.CharField(max_length=30)
    level = models.IntegerField(default=3)
    review_link = models.CharField(max_length=200)
    preview_link = models.CharField(max_length=200)
    genres = models.CharField(max_length=100)
    open_dt = models.IntegerField(blank=True, null=True)
    liked_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_movies')
    recommendation = models.ForeignKey(Recommendation, on_delete=models.SET_NULL, blank=True, null=True)


class Review(models.Model):
    content = models.CharField(max_length=140)
    score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, related_name='reviews')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
```



### articles.models

#### class Article

- 게시글을 기록하기 위한 모델 
- 등록한 유저의 정보를 저장하기 위해 user 에 user_id 를 ForeignKey 로 받음 
- 영화에 '좋아요' 를 한 유저들을 기록하기 위해 liked_users 를 M:M 필드로 생성  

#### class Comment

- 게시글에 달린 댓글을 기록하기 위한 모델 
- 등록한 유저의 정보를 저장하기 위해 user 에 user_id 를 ForeignKey 로 받음 
- secret 은 비밀 댓글의 경우 default 를 True 로 바꿔서 사용 

```python
#articles.models

from django.db import models
from django.conf import settings


class Article(models.Model):
    title = models.CharField(max_length=20)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    liked_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_articles')


class Comment(models.Model):
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    secret = models.BooleanField(default=False)
    
```



---

## 3. 오픈API (신청해놓은 상태)

### 3.1 영화정보조회 API(KMDB)

-   https://www.koreafilm.or.kr/main#none 

- [참고] 

  [https://somjang.tistory.com/entry/KMDb%EC%A0%9C%EA%B3%B5-%EC%98%81%ED%99%94-%EC%83%81%EC%84%B8%EC%A0%95%EB%B3%B4-API-%EC%9D%B8%EC%A6%9D%ED%82%A4-%EB%B0%9C%EA%B8%89%EB%B0%9B%EA%B8%B0](https://somjang.tistory.com/entry/KMDb제공-영화-상세정보-API-인증키-발급받기) 

  

- 차선책: 네이버, 영진위

  

### 3.2 유튜브 API

- https://console.developers.google.com/apis/credentials?hl=ko&pli=1&project=idyllic-folio-258707&folder&organizationId 

  
```

```

```

```

------

## ?.View

### movies.views

#### movielevellist

- 사용자의 레벨과 같은 레벨의 영화 리스트를 보여주는 함수 
- 운영자는 모든 영화가 나옴

```python
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
```



#### like

- 사용자가 영화의 좋아요를 누를 때 반응하는 함수
- 좋아요의 개수가 0이면 level 1, 1이면 level 2, 2 이상이면 level 3 이 되도록 함 

``` python
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
    # 좋아요 개수에 따라 레벨이 변합니다 
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
```



#### reviewupdate

- 영화의 리뷰를 수정하는 함수 
- 수정하기 버튼을 누르면 리뷰 수정용 폼을 보여줌
- POST 로 수정 내용을 보내면 리뷰의  내용을 수정 후 저장 

```python
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
```





# 나머지는 추가해서 올리겠습니다!퓨 ㅠㅠ


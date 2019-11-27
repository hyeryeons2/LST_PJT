from django.contrib.auth import get_user_model # 현재 활성화(active)된 user model 을 return 한다. 
from django import forms
from .models import Recommendation, Movie, Review
# from ckeditor_uploader.widgets import CKEditorUploadingWidget


class MovieForm(forms.ModelForm):

    class Meta:
        model = Movie
        fields = [
            'title', 
            'title_en', 
            'poster_url', 
            'description', 
            'running_time', 
            'directors', 
            'actors', 
            'nation', 
            'watch_grade', 
            'genres', 
            'open_dt',
            'review_link',
            'preview_link',
            'level',
            'recommendation',
        ]


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ['content', 'score', ]


class RecommendationForm(forms.ModelForm):

    class Meta:
        model = Recommendation
        fields = ['title', 'content', ]
        
from django.contrib.auth import get_user_model # 현재 활성화(active)된 user model 을 return 한다. 
from django import forms
from .models import Recommendation, Movie, Review
# from ckeditor_uploader.widgets import CKEditorUploadingWidget

class MovieForm(forms.ModelForm):

    class Meta:
        model = Movie
        fields = '__all__'
        # widgets = {
        # }


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ['content', 'score', ]

        
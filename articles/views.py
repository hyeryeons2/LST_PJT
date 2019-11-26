from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import HttpResponse, JsonResponse
from .models import Article, Comment
from .forms import ArticleForm, CommentForm


@require_GET
def index(request):
    articles = Article.objects.all()
    context = {'articles': articles}
    return render(request, 'articles/index.html', context)


@login_required
def create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid(): 
            article = form.save(commit=False)
            article.user = request.user
            article.save()
            return redirect('articles:detail', article.pk)
    form = ArticleForm()
    context = {'form': form}
    return render(request, 'articles/create.html', context)


@require_GET
def detail(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    comments = article.comments.all()
    form = CommentForm()
    context = {
        'article': article,
        'comments': comments,
        'form': form,
    }
    return render(request, 'articles/detail.html', context)


@login_required
def update(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if article.user == request.user:
        if request.method == 'POST':
            form = ArticleForm(request.POST, instance=article)
            if form.is_valid():
                form.save()
                return redirect('articles:detail', article_pk)
        else:
            form = ArticleForm(instance=article)
    else: 
        return redirect('articles:detail', article_pk)
    context = {'form':form}
    return render(request, 'articles/update.html', context)


@require_POST
def delete(request, article_pk):
    if request.user.is_authenticated:
        article = get_object_or_404(Article, pk=article_pk)
        if article.user == request.user:
            article.delete()
        else:
            return redirect('articles:detail', article_pk)
    return redirect('articles:index')


@require_POST
def comment_create(request, article_pk):
    if request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article_id = article_pk
            comment.user = request.user
            comment.save()
            return redirect('articles:detail', article_pk)


@require_POST
def comment_delete(request, comment_pk):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, pk=comment_pk)
        article_pk = comment.article_id
        article = get_object_or_404(Article, pk=article_pk)
        if comment.user == request.user or article.user == request.user:   
            comment.delete()
        return redirect('articles:detail', article_pk)
    return HttpResponse('You are Unauthorized', status=401)


@login_required
def like(request, article_pk):
    user = request.user
    article = get_object_or_404(Article, pk=article_pk)
    if article.liked_users.filter(pk=user.pk).exists():
        user.liked_articles.remove(article)
        liked = False 
    else:
        user.liked_articles.add(article)
        liked = True
    context = {
        'liked': liked, 
        'count': article.liked_users.count()
    }
    return JsonResponse(context)


@login_required
def follow(request, article_pk, user_pk):
    user = request.user
    person = get_object_or_404(get_user_model(), pk=user_pk)
    if user in person.followers.all(): 
        person.followers.remove(user)  
    else:
        person.followers.add(user) 
    return redirect('articles:detail', article_pk)

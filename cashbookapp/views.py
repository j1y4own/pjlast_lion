from django.contrib import messages
import datetime
from .models import Cashbook, Comment, Hashtag
from django.utils import timezone
from email import message
from multiprocessing import context, reduction
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CashbookForm, CommentForm, HashtagForm
from django.http import request
from django.db.models import Q
# Create your views here.


def main(request):
    return render(request, 'main.html')


def write(request, cashbook=None):
    # context = {}
    if request.method == 'POST':
        form = CashbookForm(request.POST, request.FILES, instance=cashbook,)
        if form.is_valid():
            author = request.user
            cashbook = form.save(commit=False)
            cashbook.created_at = timezone.now()
            cashbook.author = request.user
            cashbook.save()
            form.save_m2m()
            content = request.POST.get('content')
            list_hashtag = content.split(' ')
            form.save_m2m()
            for Hash in list_hashtag:
                if '#' in Hash:
                    hashtag = Hashtag()
                    hashtag.hashtag_content = Hash
                    cashbook_ = Cashbook.objects.get(id=cashbook.id)
                    cashbook_.tagging.add(hashtag)
            return redirect('read')
        else:
            return render(request, 'read.html', context)
    else:
        form = CashbookForm(instance=cashbook)
        return render(request, 'write.html', {'form': form})

def read(request):
    cashbooks = Cashbook.objects
    sort = request.GET.get('sort', '')
    if sort == 'date':
        cashbooks = Cashbook.objects.all().order_by('-created_at')
    elif sort == 'like_count':
        cashbooks = Cashbook.objects.all().order_by('-like_count')
    else:
        cashbooks = Cashbook.objects
    return render(request, 'read.html', {'cashbooks': cashbooks})


def edit(request, id):
    cashbooks = get_object_or_404(Cashbook, id=id)
    if request.method == "POST":
        form = CashbookForm(request.POST, request.FILES, instance=cashbooks,)
        if form.is_valid():
            form.save(commit=False)
            form.save()
            return redirect('read')

    else:
        form = CashbookForm(instance=cashbooks)
        return render(request, 'edit.html', {'form': form, 'cashbooks': cashbooks})


def delete(request, id):
    cashbooks = get_object_or_404(Cashbook, id=id)
    cashbooks.delete()
    return redirect('read')


def detail(request, id):
    cashbooks = get_object_or_404(Cashbook, id=id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.cashbook_id = cashbooks
            comment.author = request.user
            comment.hashtag()
            comment.text = form.cleaned_data['text']
            comment.save()
            form.save_m2m()
            id = id
            return redirect('read', id)
    else:
        form = CommentForm()
        return render(request, 'detail.html', {'cashbooks': cashbooks, 'form': form})


def update_comment(request, id, com_id):
    post = get_object_or_404(Cashbook, id=id)
    comment = get_object_or_404(Comment, id=com_id)
    form = CommentForm(instance=comment)
    if request.method == "POST":
        update_form = CommentForm(request.POST, instance=comment)
        if update_form.is_valid():
            comment = update_form.save(commit=False)
            comment.author = request.user
            comment.post_id = post
            comment.content = update_form.cleaned_data['text']
            update_form.save()
            return redirect('detail', id)
    return render(request, 'update_comment.html', {'form': form, 'post': post, 'comment': comment})


def delete_comment(request, id, com_id):
    comment = get_object_or_404(Comment, id=com_id)
    comment.delete()
    return redirect('detail', id)


def likes(request, id):
    like_b = get_object_or_404(Cashbook, id=id)
    if request.user in like_b.post_like.all():
        like_b.post_like.remove(request.user)
        like_b.like_count -= 1
        like_b.save()
    else:
        like_b.post_like.add(request.user)
        like_b.like_count += 1
        like_b.save()
    return redirect('detail', like_b.id)


def main_hashtag(request):
    hashtags = Hashtag.objects.all()
    return render(request, 'main_hashtag.html', {'hashtags': hashtags})


def detail_hashtag(request, id, hashtag_id):
    hashtags = get_object_or_404(Hashtag, id=id)
    hashtag = Hashtag.objects.filter(name=hashtags)
    hashtag_posts = Cashbook.objects.filter(hashtags__in=hashtag)
    return render(request, 'detail_hashtag.html', {'hashtag': hashtag, 'hashtag_posts': hashtag_posts})


def hashtag(request, hashtag=None):
    if request.method == 'POST':
        form = HashtagForm(request.POST, instance=hashtag)
        if form.is_valid():
            hashtag = form.save(commit=False)
            if Hashtag.objects.filter(name=form.cleaned_data['name']):
                form = HashtagForm()
                error_message = '이미 존재하는 해시태그입니다.'
                return render(request, 'hashtag.html', {'form': form, 'error_message': error_message})
            else:
                hashtag.name = form.cleaned_data['name']
                hashtag.save()
            return redirect('read')
    else:
        form = HashtagForm(instance=hashtag)
        return render(request, 'hashtag.html', {"form": form})

def search(request):
    cashbooks = Cashbook.objects.all()
    search = request.GET.get('search', '')
    if search:
        cashbooks = cashbooks.filter(
            Q(title__icontains = search) |
            Q(content__icontains = search)
            
        ).distinct()
        return render(request, 'search.html', {'cashbooks':cashbooks, 'search': search})
    else:
        return render(request, 'search.html')
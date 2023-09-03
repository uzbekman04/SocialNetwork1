from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from . import models
from accounts.models import Profile
from .forms import PostForm, CommentForm
from django.views import generic
from django.urls import reverse


def AllView(request):
    if request.user.is_authenticated:
        posts = []
        try:
            profile = Profile.objects.get(user=request.user)
        except:
            profile = Profile.objects.create(user=request.user)
            profile.save()
        for user in profile.follows.all():
            posts.append(models.Post.objects.filter(user=user))
        return render(request, 'index.html', context={"posts": posts})
    else:
        return redirect('login')


def AboutView(request, pk):
    if request.user.is_authenticated is None:
        return redirect('login')
    else:
        post = models.Post.objects.get(pk=pk)
        total_likes = post.total_likes()

        liked = False
        if post.likes.filter(id=request.user.id).exists():
            liked = True

        comments = models.Comment.objects.filter(post=post)

        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.commenter = request.user.profile
                comment.post = post
                comment.save()
                return redirect('about', pk=post.pk)
        else:
            form = CommentForm()

        context = {
            'post': post,
            'form': form,
            'comments': comments,
            'total_likes': total_likes,
            'liked': liked
        }
        return render(request, 'post1.html', context=context)


def EditView(request):
    if request.user.is_authenticated is None:
        return redirect('login')
    else:
        if request.method == 'POST':
            form = PostForm()
            if form.is_valid():
                form = PostForm(request.POST)
            return render(request, 'post1.html', context={"form": form})


class DeleteView(generic.edit.DeleteView):
    model = models.Post
    success_url = reverse_lazy('home')
    template_name = 'delete.html'

def LikeView(request, pk):
    post = get_object_or_404(models.Post, id=request.POST.get('post_id'))

    liked = False
    if post.likes.filter(id = request.user.id).exists():
        post.likes.remove(request.user.profile)
        liked = False
    else:
        post.likes.add(request.user.profile)
        liked = True

    return HttpResponseRedirect(reverse('about', args=[str(pk)]))
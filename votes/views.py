from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Post, Option, Vote
from .forms import PostForm, VoteForm


def home(request):
    posts = Post.objects.all()
    active_posts = [post for post in posts if post.is_active()]
    return render(request, 'votes/home.html', {'posts': active_posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    has_voted = False
    user_vote = None
    vote_results = []

    if request.user.is_authenticated:
        try:
            user_vote = Vote.objects.get(user=request.user, post=post)
            has_voted = True
        except Vote.DoesNotExist:
            pass

    if has_voted or not post.is_active():
        total_votes = Vote.objects.filter(post=post).count()
        options = Option.objects.filter(post=post)

        for option in options:
            option_votes = Vote.objects.filter(option=option).count()
            percentage = (option_votes / total_votes * 100) if total_votes > 0 else 0
            vote_results.append({
                'option': option,
                'votes': option_votes,
                'percentage': round(percentage, 1)
            })

    return render(request, 'votes/post_detail.html', {
        'post': post,
        'has_voted': has_voted,
        'user_vote': user_vote,
        'vote_results': vote_results
    })


@login_required
def vote(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if not post.is_active():
        return redirect('post_detail', pk=pk)

    try:
        Vote.objects.get(user=request.user, post=post)
        return redirect('post_detail', pk=pk)
    except Vote.DoesNotExist:
        pass

    if request.method == 'POST':
        form = VoteForm(request.POST, post=post)
        if form.is_valid():
            vote = form.save(commit=False)
            vote.user = request.user
            vote.post = post
            vote.save()
            return redirect('post_detail', pk=pk)
    else:
        form = VoteForm(post=post)

    return render(request, 'votes/vote.html', {'form': form, 'post': post})


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user_created = request.user
            post.save()

            options_text = request.POST.get('options', '')
            options_list = [opt.strip() for opt in options_text.split(',') if opt.strip()]

            for option_text in options_list:
                Option.objects.create(description=option_text, post=post)

            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()

    return render(request, 'votes/create_post.html', {'form': form})
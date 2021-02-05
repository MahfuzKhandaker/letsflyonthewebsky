from django.db.models import Count
from django.shortcuts import render

from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect
from blog.models import Post, Comment, Category
from django.contrib import messages
from django.http import HttpResponseRedirect, Http404, JsonResponse, HttpResponse
from django.contrib.contenttypes.models import ContentType
from blog.forms import PostForm, CommentForm
from blog.utils import get_read_time
from django.contrib.auth.models import Permission
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.urls import reverse
from django.views import generic
from django.template.loader import render_to_string
from django.db.models import Q
from django.core import serializers
from django.http import HttpResponse
try:
    from django.utils import simplejson as json
except ImportError:
    import json
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST


class Blogs(generic.ListView):
    model = Post
    # context_object_name = 'posts'
    template_name = 'blog/blog_index.html'
    paginate_by = 10


    def get_context_data(self, **kwargs):
        context = super(Blogs, self).get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
        context['post_num'] = Post.objects.filter(published_date__lte=timezone.now()).count()
        context['most_recent'] = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')[:3]
        context['blog_by_category_count']  = Post.objects.filter(published_date__lte=timezone.now()).values('categories__name').annotate(Count('categories__name')).order_by('categories')
        return context

        
class SearchResultsListView(generic.ListView):
    model = Post
    template_name = 'blog/search_results.html'
    context_object_name = 'post_list'
    
    def get_queryset(self):
        query = self.request.GET.get('q')
        return Post.objects.filter(published_date__lte=timezone.now()).filter(
            Q(title__icontains=query) | Q(categories__name__icontains=query)
        )


class DraftListView(generic.ListView):
    # redirect_field_name = 'blog/posts'
    model = Post
    template_name = 'blog/post_draft_list.html'
    context_object_name = 'draft_post'

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('created_on')

    # def get_context_data(self, **kwargs):
    #     context = super(DraftListView, self).get_context_data(**kwargs)
    #     context['draft_post'] = Post.objects.filter(published_date__isnull=True).order_by('created_on')
    #     return context

@login_required
def post_publish(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.publish()
    return redirect('blog_detail', slug=slug)


def blog_category(request, category):
    posts = Post.objects.filter(published_date__lte=timezone.now()).filter(
        categories__name__contains=category
    ).order_by(
        '-created_on'
    )
    context = {
        'category': category,
        'posts': posts
    }
    return render(request, 'blog/blog_category.html', context)


def blog_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.number_of_views = post.number_of_views+1
    post.save()

    comments = Comment.objects.filter(post=post, reply=None).order_by('-id')
    
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        is_liked = True

    is_favourite = False
    if post.favourite.filter(id=request.user.id).exists():
        is_favourite = True

    if request.method=='POST':
        querydict = request.POST
        comment_form = CommentForm(querydict)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.reply_id = querydict.get('comment_id')
            comment.save()
    else:
        comment_form = CommentForm()

    context = {
        'post': post,
        'is_liked': is_liked,
        'is_favourite': is_favourite,
        'comments': comments,
        'total_likes': post.likes.count(),
        'total_comments': post.comments.count(),
        'comment_form': comment_form,
    }
    if request.is_ajax():
        html = render_to_string('blog/comment_section.html', context, request=request)
        comments = serializers.serialize('json', list(comments), fields=('content', 'reply', 'post', 'user__username'))
        return JsonResponse({'form': html, 'comments': comments})

    return render(request, 'blog/blog_detail.html', context)

# class PostDetailView(generic.DetailView):
#     model = Post
#     context_object_name = 'post'
#     template_name = 'blog/blog_detail.html'

#     def get_context_data(self, *args, **kwargs):
#         context = super(PostDetailView, self).get_context_data(*args, **kwargs)
#         post = get_object_or_404(Post, slug=self.kwargs['slug'])
#         context['total_likes'] = post.likes.count()
#         return context


def post_favourite_list(request):
    user = request.user
    favourite_posts = user.favourite.all()
    context = {
        'favourite_posts': favourite_posts,
    }
    return render(request, 'blog/post_favourite_list.html', context)

def favourite_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.favourite.filter(id=request.user.id).exists():
        post.favourite.remove(request.user)
    else:
        post.favourite.add(request.user)
    return HttpResponseRedirect(post.get_absolute_url())

def like_post(request):
    post = get_object_or_404(Post, id=request.POST['post_id'])
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        is_liked = False
    else:
        post.likes.add(request.user)
        is_liked = True

    context ={
        'post': post,
        'is_liked': is_liked,
        'total_likes': post.likes.count(),
    }
    if request.is_ajax():
        html = render_to_string('blog/like_section.html', context, request=request)
        return JsonResponse({'form': html})
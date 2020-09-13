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

    form = CommentForm(request.POST or None)
    if form.is_valid():
        if not request.user.is_authenticated:
            return redirect('account_login')
        content_type = post.get_content_type
        object_id = post.id
        content_data = form.cleaned_data['content']

        parent_obj = None
        try:
            parent_id = int(request.POST.get('parent_id'))
        except:
            parent_id = None
    
        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists():
                parent_obj = parent_qs.first()
        
        Comment.objects.get_or_create(
            user=request.user,
            content_type=content_type,
            object_id=object_id,
            content=content_data,
            parent=parent_obj
        )
    
    
    form = CommentForm()
    # comments = Comment.objects.filter_by_instance(instance)
    comments = post.comments

    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        is_liked = True

    context = {
        'post': post,
        'is_liked': is_liked,
        'total_likes': post.likes.count(),
        'comments': comments,
        'comment_form': form,
    }
    return render(request, 'blog/blog_detail.html', context)

def post_likes(request):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
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
    # return HttpResponseRedirect(post.get_absolute_url())

@login_required
def comment_delete(request, pk):
    try:
        obj = Comment.objects.get(pk=pk)
    except:
        raise Http404

    if obj.user != request.user:
        response = HttpResponse("You do not have permission to delete this comment.")
        response.status_code = 403
        return response
    
    if request.method == "POST":
        parent_obj_url = obj.content_object.get_absolute_url()
        obj.delete()
        messages.success(request, "This has been deleted.")
        return HttpResponseRedirect(parent_obj_url)
    
    context = {
        "object": obj
    }
    return render(request, "blog/confirm_delete.html", context)

def comment_thread(request, pk):
    obj = get_object_or_404(Comment, pk=pk)
    
    form = CommentForm(request.POST or None)
    if form.is_valid():
        if not request.user.is_authenticated:
            return redirect('account_login')
        content_type = obj.content_object.get_content_type
        object_id = obj.content_object.id
        content_data = form.cleaned_data['content']
        parent_obj = None
        try:
            parent_id = int(request.POST.get('parent_id'))
        except:
            parent_id = None
            
        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists():
                parent_obj = parent_qs.first()
        
        Comment.objects.get_or_create(
            user=request.user,
            content_type=content_type,
            object_id=object_id,
            content=content_data,
            parent=parent_obj
        )
        form = CommentForm()
       
    context = {
        'comment': obj,
        'form': form
    }
    return render(request, 'blog/comment_thread.html', context)

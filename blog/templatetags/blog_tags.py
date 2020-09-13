from django import template
from django.db.models import Count
from blog.models import Post
from django.utils import timezone

register = template.Library()


@register.inclusion_tag('blog/_latest_posts.html')
def latest_posts():
    posts           = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')[:3]
    category_count  = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date').values('categories__name').annotate(Count('categories__name'))
    return {
        'posts': posts,
        'category_count': category_count
        }

from django.shortcuts import render
from django.views import generic
from django.utils import timezone
from blog.models import Post
from pages.models import About


class HomePageView(generic.ListView):
    model = Post
    template_name = 'pages/home.html'
    paginate_by = 6


    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
        context['post_num'] = Post.objects.filter(published_date__lte=timezone.now()).count()
        context['most_recent'] = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')[:3]
        return context


def about_view(request):
    about_instance = About.objects.all()
    context = {
        'about_instance': about_instance
    }
    return render(request, 'pages/about.html', context)

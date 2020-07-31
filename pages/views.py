from django.shortcuts import render
from django.views import generic
from blog.models import Post
from pages.models import About


class HomePageView(generic.ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'pages/home.html'
    paginate_by = 2


    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['post_num'] = Post.objects.count()
        return context


def about_view(request):
    about_instance = About.objects.all()
    context = {
        'about_instance': about_instance
    }
    return render(request, 'pages/about.html', context)

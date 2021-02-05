from django.urls import path
from blog import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.Blogs.as_view(), name='posts'),
    path('drafts/', views.DraftListView.as_view(), name='post_draft_list'),
    path('search/', views.SearchResultsListView.as_view(), name='search_results'), 
    path('favourites/', views.post_favourite_list, name='post_favourite_list'),
    path('like/', views.like_post, name='like_post'),
    path('<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('<slug:slug>/favourite_post/', views.favourite_post, name='favourite_post'),
    # path('<slug:slug>/likes/', views.likes, name='likes'),
    path('<category>', views.blog_category, name="blog_category"),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
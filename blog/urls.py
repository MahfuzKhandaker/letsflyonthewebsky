from django.urls import path
from blog import views

urlpatterns = [
    path('', views.Blogs.as_view(), name='posts'),
    # path('like/', views.like_post, name='like_post'),
    path('drafts/', views.DraftListView.as_view(), name='post_draft_list'),
    path('search/', views.SearchResultsListView.as_view(), name='search_results'), 
    path('<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('<slug:slug>/like/', views.post_likes, name='post_likes'),
    path('comments/<int:pk>/', views.comment_thread, name='comment_thread'),
    path('comments/<int:pk>/delete/', views.comment_delete, name='comment_delete'),
    path('<category>', views.blog_category, name="blog_category"),
]
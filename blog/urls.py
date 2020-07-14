from django.urls import path
from . import views

urlpatterns = [
    path('', views.Blogs.as_view(), name='posts'),
    path('search/', views.SearchResultsListView.as_view(), name='search_results'), 
    path('<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('comments/<int:pk>/', views.comment_thread, name='comment_thread'),
    path('comments/<int:pk>/delete/', views.comment_delete, name='comment_delete'),
    path('<category>', views.blog_category, name="blog_category"),
]
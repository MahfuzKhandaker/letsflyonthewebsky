from django.urls import path

from .views import HomePageView, about_view

urlpatterns = [
    path('about/', about_view, name='about'),
    path('', HomePageView.as_view(), name='home'),
]

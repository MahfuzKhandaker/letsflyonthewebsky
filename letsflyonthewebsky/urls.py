"""letsflyonthewebsky URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

# from blog.views import likes

urlpatterns = [
    # Django admin
    path('anything-but-admin/', admin.site.urls),

    # User management
    path('accounts/', include('allauth.urls')),
    
    # Local apps
    path('', include('pages.urls')),
    path('blog/', include('blog.urls')),
    # path('likes/', likes, name='likes'),
    path('contact/', include('contact.urls')),
    path('projects/', include('projects.urls')),
    path('newsletters/', include('newsletters.urls', namespace='newsletters')),
    path('newsletter_control/', include('newsletter_control_panel.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG: # new
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
] + urlpatterns
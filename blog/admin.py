from django.contrib import admin

from .models import Post, Category, Comment

from blog.forms import PostForm


class PostAdmin(admin.ModelAdmin):

    list_display = ('title', 'created_on', 'published_date')
    list_filter = ('created_on', 'last_modified', 'published_date')
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}
    form = PostForm
    fields = ['title', 'slug', 'summary', 'body', 'main_image', 'categories', 'published_date', 'likes']
    

class CategoryAdmin(admin.ModelAdmin):
    pass

admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment)
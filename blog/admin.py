from django.contrib import admin

from .models import Post, Category, Comment

from blog.forms import PostForm


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'status', 'created_on')
    list_filter = ("status",)
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}
    form = PostForm
    fields = ['title', 'slug', 'body', 'main_image', 'categories', 'status']
    
    
class CategoryAdmin(admin.ModelAdmin):
    pass

admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment)
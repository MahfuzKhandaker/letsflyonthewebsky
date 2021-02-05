from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save
from django.urls import reverse
from blog.utils import get_read_time
from django.utils import timezone
from django.utils.safestring import mark_safe


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    dob = models.DateField(null=True, blank=True)
    photo = models.ImageField(null=True, blank=True)


    def __str__(self):
        return "Profile of user {}".format(self.user.username)

class Category(models.Model):
    name = models.CharField(max_length=20, db_index=True,unique=True)

    objects = models.Manager()

    def __str__(self): 
        return self.name

    class Meta:
        ordering = ['-name']
        verbose_name_plural = 'categories'


class Author(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile_picture = models.ImageField()

    objects = models.Manager()

    def __str__(self):
        return self.user.username

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status="published")
        

class Post(models.Model):
    objects     = models.Manager()    #Default Manager
    published   = PublishedManager()  #Custom Model Manager

    STATUS_CHOICES = (
        ('draft','Draft'),
        ('published','Published'),
    )

    main_image      = models.ImageField(upload_to='images/', blank=True)
    image_caption   = models.CharField(max_length=125, blank=True, null=True)
    title           = models.CharField(max_length=125)
    slug            = models.SlugField(null=False, unique=True)
    author          = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='posts')
    summary         = models.CharField(max_length=255, null=True, blank=True)
    body            = models.TextField()
    created_on      = models.DateTimeField(auto_now_add=True)
    published_date  = models.DateTimeField(blank=True, null=True)
    last_modified   = models.DateTimeField(auto_now=True)
    categories      = models.ManyToManyField('Category', related_name='posts')
    read_time       = models.IntegerField(default=0)
    number_of_views = models.IntegerField(default=0, null=True, blank=True) 
    likes           = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='likes')
    featured        = models.BooleanField()
    status          = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    favourite       = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='favourite', blank=True)
    

    class Meta: 
        ordering = ['-id']
   
    def __str__(self): 
        return self.title

    def get_absolute_url(self):
        return reverse('blog_detail', kwargs={'slug': self.slug})



def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if instance.body:
        html_string = instance.body
        read_time_var = get_read_time(html_string)
        instance.read_time = read_time_var
pre_save.connect(pre_save_post_receiver, sender=Post)
       

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField(max_length=1000)
    reply = models.ForeignKey('Comment', on_delete=models.CASCADE, related_name='replies', null=True, blank=True, default=None)
    post = models.ForeignKey(
        'Post', related_name='comments', on_delete=models.CASCADE)

    objects = models.Manager()

    class Meta: 
        ordering = ['-timestamp']

    def __str__(self):
        return '{}-{}'.format(self.post.title, str(self.user.username))

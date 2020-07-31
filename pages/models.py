from django.db import models

# Create your models here.
class About(models.Model):
    profile_pic = models.ImageField(upload_to='images/', blank=True)
    name        = models.CharField(max_length=120)
    title       = models.CharField(max_length=120)
    bio         = models.CharField(max_length=250)
    description = models.TextField()
    website     = models.URLField(blank=True, null=True)

    objects = models.Manager()

    def __str__(self):
        return self.name
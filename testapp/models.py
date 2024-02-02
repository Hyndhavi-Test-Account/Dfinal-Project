from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

class CustomManger(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(atatus='published')

# Create your models here.
class Blog(models.Model):
    STATUS_CHOICES=(('draft', 'Draft'),('published','Published'))
    title = models.CharField(max_length=256)
    slug = models.SlugField(max_length=256, unique_for_date='publish')
    author = models.ForeignKey(User, related_name='blog_posts',on_delete=models.DO_NOTHING,)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    atatus = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    objects = CustomManger()

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def url(self):
        return reverse('post', args=[self.publish.year, self.publish.strftime('%m'), self.publish.strftime('%d'), self.slug])

class Comments(models.Model):
    post = models.ForeignKey(Blog, related_name="comments", on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=40)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    class Meta:
        ordering = ('-created',)
    def __str__(self):
        return f"Commented by {self.name} on {self.post}"

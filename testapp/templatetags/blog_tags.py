from testapp.models import Blog
from django import template
from django.contrib.auth.decorators import login_required
from django.db.models import Count

register = template.Library()

@register.simple_tag
def total_posts():
    return Blog.objects.count()
@login_required()
@register.inclusion_tag('testapp/list.html')
def post_list(count=10):
    list = Blog.objects.order_by('-publish',)[:9]
    return {'list':list}


# def most_commented_post(count=5):
#     return Blog.objects.annotate(total_commentss=Count('comments')).order_by('-total_comments')[:count]
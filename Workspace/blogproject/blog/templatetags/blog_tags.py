from django import template
from ..models import Post, Category

register = template.Library()

@register.simple_tag
def get_recent_posts(num=5):
    return Post.objects.all()[:num]
    
@register.simple_tag
def archives():
    return Post.objects.dates('created_time', 'month', order='DESC')
    
@register.simple_tag
def get_categories():
    #别忘了在顶部引入Category类
    return Category.objects.all()
    
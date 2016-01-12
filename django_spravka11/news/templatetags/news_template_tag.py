from news.models import Category, News
from django import template

register = template.Library()

@register.inclusion_tag('news/category_menu.html')
def category_list_menu():
    return {
        'category_list': Category.objects.all(),
    }

@register.inclusion_tag('news/last_news.html')
def last_news():
    return {
        'news_list': News.objects.filter(photo__isnull=False).order_by('-pub_date')[:5],
    }
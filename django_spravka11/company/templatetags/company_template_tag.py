from company.models import CompanyNews, Company
from django import template
from django.conf import settings

register = template.Library()

@register.inclusion_tag('company/company_news_tag_list.html')
def company_news_list():
    return {
        'companynews_list': CompanyNews.objects.all()[:5],
        'MAIN_DOMAIN': settings.MAIN_DOMAIN,
    }

@register.inclusion_tag('company/error_form.html')
def company_form_error(company):
    return {
        'company': company,
    }

@register.inclusion_tag('company/back_call_form.html')
def company_form_back_call(company):
    return {
        'company': company,
    }

@register.inclusion_tag('company/ads_link.html')
def company_ads_link():
    return {
        'company': 1,
    }
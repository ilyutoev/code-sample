from math import ceil
import json
from zipfile import *
import os
import re
from itertools import chain
from django.shortcuts import render, Http404, render_to_response
from django.views.generic import ListView, DetailView
from django.contrib.admin.views.decorators import staff_member_required
from django.template import RequestContext
from django.db.models import Max
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMessage
from haystack.query import SearchQuerySet

from company.models import Category, Company, Address, CompanyNews, CompanyService, CompanyImage, CompanyPage, Timetable, Phone, SeoCategory
from .forms import UploadFileImportForm
from spravka11.settings import MEDIA_ROOT
from misc.models import Autocomplete


def site_index(request):
    list_level0 = SeoCategory.objects.filter(level=0).values_list('pk', flat=True)
    part1 = list_level0[:int(len(list_level0)/2)]
    part2 = list_level0[int(len(list_level0)/2):]

    cat1 = SeoCategory.objects.filter(pk__in=part1) | SeoCategory.objects.filter(parent__pk__in=part1)
    cat2 = SeoCategory.objects.filter(pk__in=part2) | SeoCategory.objects.filter(parent__pk__in=part2)

    context = {'seo_category1': cat1}
    context['seo_category2'] = cat2

    temp_company_logo = Company.objects.filter(logo__isnull=False, recomendation=True).order_by('?')

    row_count = 3
    i = ceil(len(temp_company_logo)/row_count)
    pl = []
    for x in range(i):
        pl.append(temp_company_logo[x*row_count:x*row_count+row_count])
    context['logo_company'] = pl

    context['is_index'] = True
    return render(request, 'company/index.html', context)


class SeoCompanyList(ListView):
    template_name = 'company/seo_company_list.html'
    paginate_by = 10
    count = 0

    def get_queryset(self):
        temp_id = Address.objects.filter(seo_category=self.args[0]).values('company', 'city').distinct().annotate(Max('id')).values_list('id__max', flat=True)

        company = Address.objects.filter(pk__in=temp_id).order_by('-company__yellow',
                                                                  '-company__blue',
                                                                  '-company__priority',
                                                                  'company__name')

        self.count = company.count()
        return company

    def get_context_data(self, **kwargs):
        context = super(SeoCompanyList, self).get_context_data(**kwargs)
        context['category'] = SeoCategory.objects.get(pk=self.args[0])
        context['category_list'] = SeoCategory.objects.filter(parent=self.args[0])
        context['count'] = self.count
        return context


def category_index(request):
    list_level0 = Category.objects.filter(level=0).values_list('pk', flat=True)
    part1 = list_level0[:int(len(list_level0)/2)]
    part2 = list_level0[int(len(list_level0)/2):]

    cat1 = Category.objects.filter(pk__in=part1) |\
           Category.objects.filter(parent__pk__in=part1) |\
           Category.objects.filter(parent__parent__pk__in=part1)
    cat2 = Category.objects.filter(pk__in=part2) |\
           Category.objects.filter(parent__pk__in=part2) |\
           Category.objects.filter(parent__parent__pk__in=part2)

    context = {'category1': cat1}
    context['category2'] = cat2

    context['abc'] = abc

    return render(request, 'company/category_index.html', context)


class CompanyList(ListView):
    template_name = 'company/company_list.html'
    paginate_by = 10
    count = 0

    def get_queryset(self):
        temp_id = Address.objects.filter(category=self.args[0]).values('company', 'city').distinct().annotate(Max('id')).values_list('id__max', flat=True)
        company = Address.objects.filter(pk__in=temp_id).order_by('-company__yellow',
                                                                  '-company__blue',
                                                                  '-company__priority',
                                                                  'company__name')

        self.count = company.count()
        return company

    def get_context_data(self, **kwargs):
        context = super(CompanyList, self).get_context_data(**kwargs)
        context['category'] = Category.objects.get(pk=self.args[0])
        context['category_list'] = Category.objects.filter(parent=self.args[0])
        context['count'] = self.count
        return context


class CategoryABCList(ListView):
    template_name = 'company/abc_list.html'
    model = Category
    global abc
    abc = {0: 'А', 1: 'Б', 2: 'В', 3: 'Г', 4: 'Д', 5: 'Е', 6: 'Ж', 7: 'З', 8: 'И', 9: 'К', 10: 'Л', 11: 'М', 12: 'Н', 13: 'О', 14: 'П', 15: 'Р', 16: 'С', 17: 'Т', 18: 'У', 19: 'Ф', 20: 'Х', 21: 'Ц', 22: 'Ч', 23: 'Ш', 24: 'Щ', 25: 'Э', 26: 'Ю', 27: 'Я', 30: 'Все'}

    def get_queryset(self):
        if self.args:
            try:
                value = int(self.args[0])
            except ValueError:
                value = 777
            if value in abc:
                if value == 30:
                    return Category.objects.filter(level=2).order_by('name')
                else:
                    return Category.objects.filter(name__startswith=abc[value], level=2).order_by('name')
            else:
                raise Http404
        else:
            return Category.objects.filter(level=2).order_by('name')

    def get_context_data(self, **kwargs):
        context = super(CategoryABCList, self).get_context_data(**kwargs)
        context['abc'] = abc
        value = int(self.args[0])
        context['leter'] = abc[value]
        return context


class CompanyDetail(DetailView):
    model = Company
    template_name = 'company/detail.html'

    def get_template_names(self):
        temp = Company.objects.get(pk=int(self.kwargs['pk']))
        if temp.vizitka:
            return 'company/vizitka_index.html'
        else:
            return self.template_name
    
    def get_context_data(self, **kwargs):
        context = super(CompanyDetail, self).get_context_data(**kwargs)
        company = Company.objects.get(pk=int(self.kwargs['pk']))
        company.counter = company.counter + 1
        company.save()

        try:
            context['cookie_city'] = self.request.session['city']

            if context['cookie_city'] == 'Все города':
                first_path = Address.objects.filter(company=company, city__name='Сыктывкар')
                second_path = Address.objects.filter(company=company).exclude(city__name='Сыктывкар')
                context['city_address'] = chain(first_path, second_path)
                context['common_company'] = company.common_company()
            else:
                first_path = Address.objects.filter(company=company, city__name=self.request.session['city'])
                second_path = Address.objects.filter(company=company).exclude(city__name=self.request.session['city'])
                context['city_address'] = chain(first_path, second_path)
                context['common_company'] = company.common_company(city=self.request.session['city'])
        except:
            context['cookie_city'] = ''
            context['city_address'] = Address.objects.filter(company=company)
            context['common_company'] = company.common_company()

        return context


class CompanyNewsAll(ListView):
    model = CompanyNews
    template_name = 'company/company_news_list.html'
    paginate_by = 10


class CompanyNewsDetail(DetailView):
    model = CompanyNews
    template_name = 'company/vizitka_news_detail.html'

    def get_object(self, **kwargs):
        if self.kwargs:
            try:
               return CompanyNews.objects.get(pk=int(self.kwargs['news_pk']), company__pk=int(self.kwargs['company_pk']))
            except:
                raise Http404

    def get_context_data(self, **kwargs):
        context = super(CompanyNewsDetail, self).get_context_data(**kwargs)
        context['company'] = Company.objects.get(pk=int(self.kwargs['company_pk']))
        return context


class CurrentCompanyNewsAll(ListView):
    model = CompanyNews
    template_name = 'company/vizitka_news_list.html'
    paginate_by = 10

    def get_queryset(self, **kwargs):
        companynews = CompanyNews.objects.filter(company=int(self.kwargs['company_pk']))
        if companynews:
            return companynews 
        else:
            raise Http404

    def get_context_data(self, **kwargs):
        context = super(CurrentCompanyNewsAll, self).get_context_data(**kwargs)
        context['company'] = Company.objects.get(pk=int(self.kwargs['company_pk']))
        return context


class CurrentCompanyService(ListView):
    model = CompanyService
    template_name = 'company/vizitka_service_list.html'

    def get_queryset(self, **kwargs):
        companylist = CompanyService.objects.filter(company=int(self.kwargs['company_pk']))
        if companylist:
            return companylist
        else:
            raise Http404

    def get_context_data(self, **kwargs):
        context = super(CurrentCompanyService, self).get_context_data(**kwargs)
        context['company'] = Company.objects.get(pk=int(self.kwargs['company_pk']))
        return context


class CompanyServiceDetail(DetailView):
    model = CompanyService
    template_name = 'company/vizitka_service_detail.html'

    def get_object(self, **kwargs):
        if self.kwargs:
            try:
               return CompanyService.objects.get(pk=int(self.kwargs['service_pk']), company__pk=int(self.kwargs['company_pk']))
            except:
                raise Http404

    def get_context_data(self, **kwargs):
        context = super(CompanyServiceDetail, self).get_context_data(**kwargs)
        context['company'] = Company.objects.get(pk=int(self.kwargs['company_pk']))
        return context


class CompanyImageAll(ListView):
    model = CompanyImage
    template_name = 'company/vizitka_photo_list.html'

    def get_queryset(self, **kwargs):
        companylist = CompanyImage.objects.filter(company=int(self.kwargs['company_pk']))
        if companylist:
            return companylist
        else:
            raise Http404

    def get_context_data(self, **kwargs):
        context = super(CompanyImageAll, self).get_context_data(**kwargs)
        context['company'] = Company.objects.get(pk=int(self.kwargs['company_pk']))
        return context


class CompanyPageView(DetailView):
    model = CompanyPage
    template_name = 'company/vizitka_page.html'

    def get_object(self, **kwargs):
        if self.kwargs:
            try:
               return CompanyPage.objects.get(slug=self.kwargs['slug'], company__pk=int(self.kwargs['company_pk']))
            except:
                raise Http404

    def get_context_data(self, **kwargs):
        context = super(CompanyPageView, self).get_context_data(**kwargs)
        context['company'] = Company.objects.get(pk=int(self.kwargs['company_pk']))
        return context


class CompanySearch(ListView):
    template_name = "company/search.html"
    paginate_by = 10
    count = 0
    q_punto = ''
    q_spell = ''

    def get_context_data(self, **kwargs):
        context = super(CompanySearch, self).get_context_data(**kwargs)
        q = self.request.GET.get('q')
        city = self.request.GET.get('city')
        context['q'] = q
        context['q_punto'] = self.q_punto
        context['q_spell'] = self.q_spell
        context['city'] = city
        context['search_results_count'] = self.count
        self.request.session['city'] = city
        return context

    def get_queryset(self):
        def fix_layout(s):
            return ''.join([_trans_table.get(c, c) for c in s])

        q = self.request.GET.get('q')
        city = self.request.GET.get('city')
        if q:
            if city == 'Все города':
                results = SearchQuerySet().filter(content=q).values_list('company', flat=True)
            else:
                results = SearchQuerySet().filter(content=q, city=city).values_list('company', flat=True)

            if results.count() == 0:
                _eng_chars = "~!@#$%^&qwertyuiop[]asdfghjkl;'zxcvbnm,./QWERTYUIOP{}ASDFGHJKL:\"|ZXCVBNM<>?"
                _rus_chars = "ё!\"№;%:?йцукенгшщзхъфывапролджэячсмитьбю.ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭ/ЯЧСМИТЬБЮ,"
                _trans_table = dict(zip(_eng_chars, _rus_chars))

                if re.fullmatch('[a-zA-Z0-9\s]*', q):
                    self.q_punto = fix_layout(q)
                    if city == 'Все города':
                        results = SearchQuerySet().filter(content=self.q_punto).values_list('company', flat=True)
                    else:
                        results = SearchQuerySet().filter(content=self.q_punto, city=city).values_list('company', flat=True)

                    if results.count() == 0:
                        sqs = SearchQuerySet().auto_query(self.q_punto)
                        self.q_spell = sqs.spelling_suggestion()
                        if city == 'Все города':
                            results = SearchQuerySet().filter(content=self.q_spell).values_list('company', flat=True)
                        else:
                            results = SearchQuerySet().filter(content=self.q_spell, city=city).values_list('company', flat=True)

                if results.count() == 0:
                    sqs = SearchQuerySet().auto_query(q)
                    self.q_spell = sqs.spelling_suggestion()
                    if city == 'Все города':
                        results = SearchQuerySet().filter(content=self.q_spell).values_list('company', flat=True)
                    else:
                        results = SearchQuerySet().filter(content=self.q_spell, city=city).values_list('company', flat=True)

                if results.count() == 0:
                    if city == 'Все города':
                        results = Company.objects.filter(name__icontains=q).values_list('pk', flat=True)
                    else:
                        results = Company.objects.filter(name__icontains=q, address__city__name=city).values_list('pk', flat=True)


            if city == 'Все города':
                temp_id = Address.objects.filter(company__in=set(results)).values('company').distinct().annotate(Max('id')).values_list('id__max', flat=True)
            else:
                temp_id = Address.objects.filter(company__in=set(results), city__name=city).values('company', 'city').distinct().annotate(Max('id')).values_list('id__max', flat=True)

            search_results = Address.objects.filter(pk__in=temp_id).order_by('-company__yellow',
                                                                             '-company__blue',
                                                                             '-company__priority',
                                                                             'company__name')

            self.count = search_results.count()
        else:
            search_results = ''
        return search_results


def autocomplete(request):
    if request.is_ajax():
        q = request.GET.get('term')
        titles = Autocomplete.objects.filter(title__icontains=q)[:5]
        results = []
        for title in titles:
            title_json = {}
            title_json['id'] = title.id
            title_json['label'] = title.title
            title_json['value'] = title.title
            results.append(title_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    return HttpResponse(data, content_type='application/json')


@csrf_exempt
def formcompanyerror(request):
    if request.method == "POST" and request.is_ajax():
        try:
            subject = 'spravka11.ru - Ошибка в компании {0}'.format(str(request.POST.get("company")))
            html_content = '<p>Ошибка в компании {0}</p><p>Текст сообщения: {1}</p><p>Автор сообщения: {2}</p><p>Его e-mail: {3}</p><p>Его телефон: {4}</p>'.format(str(request.POST.get("company")), str(request.POST.get("text")), str(request.POST.get("name")), str(request.POST.get("email")), str(request.POST.get("tel")))
            from_email = 'spravka11.ru@mail.ru'
            to = 'russevkomi@yandex.ru'
            msg = EmailMessage(subject, html_content, from_email, [to])
            msg.content_subtype = 'html'
            msg.send()
        except:
            pass
        return HttpResponse(json.dumps("success"), content_type="application/json")
    else:
        return HttpResponse('')


@csrf_exempt
def formcompanybackcall(request):
    if request.method == "POST" and request.is_ajax():
        try:
            comp = Company.objects.get(pk=int(request.POST.get("company")))
            subject = 'spravka11.ru - Обратный звонок с сайта'

            html_content = '<p>Обратный звонок с сайта spravka11.ru для компании {0}</p><p>Текст сообщения: {1}</p><p>Автор сообщения: {2}</p><p>Его e-mail: {3}</p><p>Его телефон: {4}</p>'.format(str(comp.name), str(request.POST.get("text")), str(request.POST.get("name")), str(request.POST.get("email")), str(request.POST.get("tel")))
            from_email = 'spravka11.ru@mail.ru'
            msg = EmailMessage(subject, html_content, from_email, [str(comp.email), 'russevkomi@yandex.ru'])
            msg.content_subtype = 'html'
            msg.send()
        except:
            pass

        return HttpResponse(json.dumps("success"), content_type="application/json")
    else:
        return HttpResponse('')


def addcompany(request):
    if request.method == "POST":
        try:
            subject = 'spravka11.ru - Новая компания'

            html_content = '<p>Добавлена новая компания на сайте spravka11.ru</p><p>Название компании: {0}</p><p>Сфера деятельности: {1}</p><p>Рубрика: {2}</p><p>Группы адресов: {3}</p><p>E-mail: {4}</p><p>Сайт: {5}</p><p>Комментарий: {6}</p><p>ФИО отправителя: {7}</p><p>Контакные данные отправителя: {8}</p>'.format(str(request.POST.get("name")), str(request.POST.get("work")), str(request.POST.get("cat")), str(request.POST.get("addressess")), str(request.POST.get("email")), str(request.POST.get("web")), str(request.POST.get("comment")), str(request.POST.get("fio")),  str(request.POST.get("contact")))
            from_email = 'spravka11.ru@mail.ru'
            msg = EmailMessage(subject, html_content, from_email, ['russevkomi@yandex.ru'])
            msg.content_subtype = 'html'
            msg.send()
        except:
            pass
        thanks = True
        return render(request, 'company/add_company.html', {'thanks': thanks})
    else:
        category = Category.objects.filter(level=2).order_by('name')
        return render(request, 'company/add_company.html', {'category': category})


@staff_member_required
def admin_company_import_export(request):
    if request.method == 'POST':
        form = UploadFileImportForm(request.POST, request.FILES)
        if form.is_valid():
            check_file = handle_uploaded_file(request.FILES['importfile'])
            context = {'is_file': True}
    else:
        context = {'is_file': False}
        form = UploadFileImportForm()
    
    context['form'] = form

    return render_to_response('company/admin_import.html', context, context_instance=RequestContext(request))


def handle_uploaded_file(f):
    name = MEDIA_ROOT + '/import/company/company.zip'

    if not os.path.exists(MEDIA_ROOT + '/import/company/'):
        os.mkdir(MEDIA_ROOT + '/import/company/')
    with open(name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    if is_zipfile(name):
        z = ZipFile(name, 'r')
        z.extractall(MEDIA_ROOT + '/import/company/')

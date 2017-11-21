from django.views.generic import ListView, DetailView
from django.http import Http404

from company.models import Company, CompanyNews, CompanyService, CompanyImage, CompanyPage, Timetable, Phone


class SubCompanyDetail(DetailView):
    model = Company
    template_name = 'company/vizitka_index.html'

    def get_object(self):
        company = Company.objects.get(subdomain=getattr(self.request, 'subdomain', ''))
        if company.vizitka and getattr(self.request, 'is_subdomain', False):
            return company
        else:
            raise Http404

    def get_context_data(self, **kwargs):
        context = super(SubCompanyDetail, self).get_context_data(**kwargs)
        company = Company.objects.get(subdomain=getattr(self.request, 'subdomain', ''))
        company.counter = company.counter + 1
        company.save()
        return context


class SubCurrentCompanyNewsAll(ListView):
    model = CompanyNews
    template_name = 'company/vizitka_news_list.html'
    paginate_by = 10

    def get_queryset(self, **kwargs):
        companynews = CompanyNews.objects.filter(company__subdomain=getattr(self.request, 'subdomain', ''))
        if companynews:
            return companynews 
        else:
            raise Http404

    def get_context_data(self, **kwargs):
        context = super(SubCurrentCompanyNewsAll, self).get_context_data(**kwargs)
        context['company'] = Company.objects.get(subdomain=getattr(self.request, 'subdomain', ''))
        return context


class SubCompanyNewsDetail(DetailView):
    model = CompanyNews
    template_name = 'company/vizitka_news_detail.html'

    def get_object(self, **kwargs):
        if self.kwargs:
            try:
               return CompanyNews.objects.get(pk=int(self.kwargs['news_pk']),
                                              company__subdomain=getattr(self.request, 'subdomain', ''))
            except:
                raise Http404

    def get_context_data(self, **kwargs):
        context = super(SubCompanyNewsDetail, self).get_context_data(**kwargs)
        context['company'] = Company.objects.get(subdomain=getattr(self.request, 'subdomain', ''))
        return context


class SubCompanyImageAll(ListView):
    model = CompanyImage
    template_name = 'company/vizitka_photo_list.html'

    def get_queryset(self, **kwargs):
        companyimages = CompanyImage.objects.filter(company__subdomain=getattr(self.request, 'subdomain', ''))
        if companyimages:
            return companyimages
        else:
            raise Http404

    def get_context_data(self, **kwargs):
        context = super(SubCompanyImageAll, self).get_context_data(**kwargs)
        context['company'] = Company.objects.get(subdomain=getattr(self.request, 'subdomain', ''))
        return context


class SubCurrentCompanyService(ListView):
    model = CompanyService
    template_name = 'company/vizitka_service_list.html'

    def get_queryset(self, **kwargs):
        companylist = CompanyService.objects.filter(company__subdomain=getattr(self.request, 'subdomain', ''))
        if companylist:
            return companylist
        else:
            raise Http404

    def get_context_data(self, **kwargs):
        context = super(SubCurrentCompanyService, self).get_context_data(**kwargs)
        context['company'] = Company.objects.get(subdomain=getattr(self.request, 'subdomain', ''))
        return context


class SubCompanyServiceDetail(DetailView):
    model = CompanyService
    template_name = 'company/vizitka_service_detail.html'

    def get_object(self, **kwargs):
        if self.kwargs:
            try:
               return CompanyService.objects.get(pk=int(self.kwargs['service_pk']),
                                                 company__subdomain=getattr(self.request, 'subdomain', ''))
            except:
                raise Http404

    def get_context_data(self, **kwargs):
        context = super(SubCompanyServiceDetail, self).get_context_data(**kwargs)
        context['company'] = Company.objects.get(subdomain=getattr(self.request, 'subdomain', ''))
        return context


class SubCompanyPageView(DetailView):
    model = CompanyPage
    template_name = 'company/vizitka_page.html'

    def get_object(self, **kwargs):
        if self.kwargs:
            try:
               return CompanyPage.objects.get(slug=self.kwargs['slug'],
                                              company__subdomain=getattr(self.request, 'subdomain', ''))
            except:
                raise Http404

    def get_context_data(self, **kwargs):
        context = super(SubCompanyPageView, self).get_context_data(**kwargs)
        context['company'] = Company.objects.get(subdomain=getattr(self.request, 'subdomain', ''))
        return context

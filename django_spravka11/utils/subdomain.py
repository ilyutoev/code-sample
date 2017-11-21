from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.conf import settings

from company.models import Company
from vizitka.views import SubCompanyDetail


class CompanySiteMiddleware(object):
    def process_request(self, request):
        domain_parts = request.get_host().split('.')
        if len(domain_parts) == 3:
            request.is_subdomain = True
            request.subdomain = domain_parts[0]
            try:
                Company.objects.get(subdomain=request.subdomain)
            except ObjectDoesNotExist:
                return redirect('http://{}'.format(settings.MAIN_DOMAIN))

    def process_view(self, request, view_func, view_args, view_kwargs):
        subdomain = getattr(request, 'subdomain', None)
        if subdomain and request.path == '/':
            view = SubCompanyDetail.as_view()(request, subdomain=subdomain)
            return view


def main_domain_context_processor(request):
    return {'MAIN_DOMAIN': settings.MAIN_DOMAIN}
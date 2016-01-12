from django.shortcuts import render
from django.views import generic
from datetime import datetime, timedelta
from django.http import Http404

from .models import Events, Session, EventPlace, EventType

class IndexView(generic.ListView):
    """Получаем список событий (по дате, категории), разбиваем на страницы. По списку событий строим список сессий и его выводим в шаблон + ряд перменных."""
    template_name = 'events/list.html'
    paginate_by = 10
    
    ev = []

    def get_queryset(self, **kwargs):
        date = datetime.today()
        rubr = False
        try:
            date += timedelta(days=int(self.kwargs['day']))
        except:
            pass

        try:
            rubr = int(self.kwargs['rubr_pk'])
        except:
            pass

        #выбираем только id нужных событий и возвращаем списко полученных id
        if rubr:
            self.ev = Events.objects.filter(session__date=date, event_type=rubr).distinct().values_list('id', flat=True)
        else:
            self.ev = Events.objects.filter(session__date=date).distinct().values_list('id', flat=True)

        if not self.ev:
            pass

        return list(self.ev)

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['today'] = date = datetime.today()
        rubr = False
        try:
            select_day = int(self.kwargs['day'])
            date += timedelta(days=select_day)
            context['date'] = date
            context['select_day'] = select_day
        except:
            pass

        try:
            rubr = int(self.kwargs['rubr_pk'])
            context['rubr'] = EventType.objects.get(pk=rubr)
        except:
            pass

        #костыль с разбивкой на страницы
        page = context['page_obj'].number

        temp_ev = self.ev[(page-1)*self.paginate_by:page*self.paginate_by]

        context['session_list'] = Session.objects.filter(event__in=temp_ev, date=date)
        context['afisha_menu'] = True
        return context


class DetailView(generic.DetailView):
    model = Events
    template_name = 'events/detail.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['afisha_menu'] = True
        return context

class PlaceView(generic.DetailView):
    model = EventPlace
    template_name = 'events/place.html'

    def get_context_data(self, **kwargs):
        context = super(PlaceView, self).get_context_data(**kwargs)
        context['afisha_menu'] = True
        return context
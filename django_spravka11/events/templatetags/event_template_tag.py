from events.models import EventType, Session
from django import template
from datetime import datetime, timedelta
from django.db.models import Max, Min

register = template.Library()

@register.inclusion_tag('events/eventtype_menu.html')
def eventtype_list_menu(rubr, select_day):
    today = datetime.today()
    days = map(lambda x: today + timedelta(days=x), range(1,7))
    return {
        'eventtype_list': EventType.objects.all(),
        'day_list': days,
        'today': today,
        'rubr': rubr,
        'select_day': select_day,
    }

@register.inclusion_tag('events/last_events.html')
def last_events():
    today = datetime.today()
    
    #жуткий запрос - выбираю мероприятия по дате (чтоб вышло только одно)
    ev = Session.objects.filter(date__gte=today).values('event').distinct().annotate(Min('date'),Min('event__title'), Min('event__poster')).order_by('date__min')[:5]

    return {
        'ev': ev,
    }
from datetime import datetime, timedelta
from django.db import models


class EventType(models.Model):
    title = models.CharField('Тип мероприятия', max_length=30)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'тип мероприятия'
        verbose_name_plural = 'типы мероприятий'


class EventPlace(models.Model):
    name = models.CharField('Название места', max_length=200)
    description = models.TextField('Описание места')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'место'
        verbose_name_plural = 'места'

    def place_detail(self):
        today = datetime.today()
        week_day = today + timedelta(days=6) 
        return Session.objects.filter(place=self, date__range=(today, week_day)).order_by('date','time')


class Events(models.Model):
    title = models.CharField('Название мероприятия', max_length=255)
    description = models.TextField('Описание мероприятия')
    event_type = models.ForeignKey(EventType)
    ganre = models.CharField('Жанр', blank=True, max_length=255)
    limit_year = models.CharField('Возрастное ограничение', blank=True, max_length=10)
    poster = models.ImageField('Постер', upload_to = 'events/%Y/%m/%d', null=True, default=None, blank=True)
    url = models.CharField('Ссылка с парсинга', max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'событие'
        verbose_name_plural = 'события'

    def event_detail(self):
        today = datetime.today()
        week_day = today + timedelta(days=6) 
        return Session.objects.filter(event=self, date__range=(today, week_day)).order_by('date', 'place', 'time')

    def get_images(self):
        return EventImages.objects.filter(event_id=self.id)

    @staticmethod
    def autocomplete_search_fields():
        return ('id__iexact', 'title__icontains',)


class Session(models.Model):
    event = models.ForeignKey(Events)
    place = models.ForeignKey(EventPlace, default=None)
    date = models.DateField('Дата проведения мероприятия')
    time = models.TimeField('Время проведения')
    price = models.CharField('Цена', max_length=20)

    class Meta:
        verbose_name = 'сеанс'
        verbose_name_plural = 'сеансы'
        ordering = ['event', 'place', 'date', 'time']


class EventImages(models.Model):
    event = models.ForeignKey(Events, related_name='изображения')
    image = models.ImageField('Изображения', upload_to = 'events/%Y/%m/%d', null=True, default=None)

    class Meta:
        verbose_name = 'изображение для события'
        verbose_name_plural = 'изображения для событий'

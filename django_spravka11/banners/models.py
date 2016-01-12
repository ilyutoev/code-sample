import hashlib
from datetime import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from .managers import BiasedManager

class BannerGroup (models.Model):
	name = models.CharField(verbose_name=_('Name'), max_length=255)
	slug = models.SlugField(verbose_name=_('Slug'), unique=True)

	public = models.BooleanField(verbose_name=_('Public'), default=True)
	created_at = models.DateTimeField(verbose_name=_('Created At'), auto_now_add=True)
	updated_at = models.DateTimeField(verbose_name=_('Updated At'), auto_now=True)

	def __str__(self):
		return self.name

	class Meta:
		ordering = ['name']
		verbose_name = _('Banner Group')
		verbose_name_plural = _('Banner Groups')

class Banner(models.Model):
	objects = BiasedManager()

	title = models.CharField(verbose_name=_('Title'), max_length=255, blank=True)
	alt = models.CharField(verbose_name=_('Alt'), max_length=255)

	text = models.TextField(verbose_name=_('Text'), blank=True, null=True)
	img = models.FileField(verbose_name=_('Image'), upload_to='banners', blank=True, null=True)
	url = models.CharField(verbose_name=_('URL'), max_length=1024)

	sort = models.PositiveSmallIntegerField(verbose_name=_('Sort'), default=500)

	group = models.ForeignKey(BannerGroup, related_name='banners', verbose_name=_('Group'))

	width = models.PositiveIntegerField('Ширина', blank=True, help_text='Для flash баннеров', default=0)
	height = models.PositiveIntegerField('Высота',blank=True, help_text='Для flash баннеров', default=0)

	html = models.BooleanField(verbose_name=_('Is HTML?'), default=False)
	flash = models.BooleanField(verbose_name=_('Is Flash?'), default=False)

	public = models.BooleanField(verbose_name=_('Public'), default=True)
	created_at = models.DateTimeField(verbose_name=_('Created At'), auto_now_add=True)
	updated_at = models.DateTimeField(verbose_name=_('Updated At'), auto_now=True)

	def key(slef):
		if hasattr(settings, 'SECRET_KEY'):
			key = str(datetime.now()) + settings.SECRET_KEY
		else:
			key = str(datetime.now())
		return hashlib.md5(key.encode('utf-8')).hexdigest()

	def log(self, request, type, key):
		log = {
			'type': type,
			'key': key,
			'banner': self,
			'group': self.group,
			'ip': request.META.get('REMOTE_ADDR'),
			'user_agent': request.META.get('HTTP_USER_AGENT'),
			'page': request.META.get('HTTP_REFERER'),
		}

		if request.user.is_authenticated():
			log['user'] = request.user
		return Log.objects.create(**log)

	@models.permalink
	def image(self):
		return ('banner_view', (), {'banner_id': self.pk, 'key': self.key()})

	def impressions(self):
		return Log.objects.filter(banner=self.pk, type=0).count()

	def views(self):
		return Log.objects.filter(banner=self.pk, type=1).count()

	def clicks(self):
		return Log.objects.filter(banner=self.pk, type=2).count()

	def __str__(self):
		return self.title or self.alt

	def get_absolute_url(self):
		if self.url == '#':
			return self.url
		else:
			@models.permalink
			def get_absolute_url(self):
				return ('banner_click', (), {'banner_id': self.pk, 'key': self.key()})
			return get_absolute_url(self)

	class Meta:
		ordering = ['sort']
		verbose_name = _('Banner')
		verbose_name_plural = _('Banners')

class Log(models.Model):
	banner = models.ForeignKey(Banner, related_name='banner_logs')
	group = models.ForeignKey(BannerGroup, related_name='group_logs', verbose_name=_('Group'), blank=True)

	user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, related_name='users', verbose_name=_('User'))
	datetime = models.DateTimeField(verbose_name=_('Clicked At'), auto_now_add=True)
	ip = models.IPAddressField(verbose_name=_('IP'), null=True, blank=True)
	user_agent = models.CharField(verbose_name=_('User Agent'), max_length=1024, null=True, blank=True)
	page = models.URLField(verbose_name=_('Page'), null=True, blank=True)
	key = models.CharField(verbose_name=_('User Agent'), max_length=32, null=True, blank=True)
	TYPE_CHOICES = (
		(0, 'impressions'),
		(1, 'view'),
		(2, 'click')
	)

	type = models.PositiveSmallIntegerField(verbose_name=_('Type'), max_length=1, default=0, choices=TYPE_CHOICES)

	def __str__(self):
		return '%s - (%s)' % (self.banner, self.datetime)


class LogStat(models.Model):
	banner = models.ForeignKey(Banner, related_name='banner_stat', verbose_name=_('Banner'), blank=True)
	group = models.ForeignKey(BannerGroup, related_name='group_stat', verbose_name=_('Group'), blank=True)

	date = models.DateField(verbose_name=_('Data'))
	view = models.PositiveIntegerField(verbose_name=_('Views'))
	click = models.PositiveIntegerField(verbose_name=_('Clicks'))
	unique_click = models.PositiveIntegerField(verbose_name=_('Unique Views'), blank=True, null=True)
	unique_view = models.PositiveIntegerField(verbose_name=_('Unique Clicks'))

	def __str__(self):
		return '%s - (%s)' % (self.banner, self.date)

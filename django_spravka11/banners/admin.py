from django.contrib import admin

from .models import BannerGroup
from .models import Banner
from .models import Log

class BannerAdminInline(admin.StackedInline):
	model = Banner
	extra = 1
	fields = ['public', 'title', 'url', 'img']


class BannerAdmin(admin.ModelAdmin):
	list_display = ('__str__', 'url', 'sort', 'views', 'clicks', 'public', 'created_at', 'updated_at')
	search_fields = ('title', 'url', 'sort', 'views', 'clicks', 'public', 'created_at', 'updated_at')
	list_filter = ['public']
	list_editable = ['sort', 'public']

admin.site.register(Banner, BannerAdmin)

class BannerGroupAdmin(admin.ModelAdmin):
	list_display = ('name', 'slug', 'public', 'created_at', 'updated_at')
	search_fields = ('name', 'slug', 'public', 'created_at', 'updated_at')
	list_filter = ['public']
	list_editable = ['public']
	inlines = [BannerAdminInline]

admin.site.register(BannerGroup, BannerGroupAdmin)

class LogGroupAdmin(admin.ModelAdmin):
	list_display = ('banner', 'user', 'datetime', 'ip', 'user_agent', 'page', 'type')
	search_fields = ('banner', 'user', 'datetime', 'ip', 'user_agent', 'page', 'type', 'key')
	list_filter = ('type', 'banner', 'user', 'datetime', 'ip')

admin.site.register(Log, LogGroupAdmin)

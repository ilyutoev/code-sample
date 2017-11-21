from django.contrib import admin

from events.models import Events, Session, EventPlace, EventType, EventImages


class SessionInline(admin.StackedInline):
    model = Session
    extra = 1


class ImagesInline(admin.StackedInline):
    model = EventImages
    extra = 1


class EventsAdmin(admin.ModelAdmin):
    inlines = [SessionInline, ImagesInline]
    class Media:
        js = [
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/static/grappelli/tinymce_setup/tinymce_setup.js',
        ]


class SessionAdmin(admin.ModelAdmin):
    list_display = ('event', 'date', 'time')
    raw_id_fields = ('event',)
    autocomplete_lookup_fields = {'fk': ['event']}


class EventPlaceAdmin(admin.ModelAdmin):
    class Media:
        js = [
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/static/grappelli/tinymce_setup/tinymce_setup.js',
        ]


class EventImagesAdmin(admin.ModelAdmin):
    raw_id_fields = ('event',)
    autocomplete_lookup_fields = {'fk': ['event']}


admin.site.register(Events, EventsAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(EventPlace, EventPlaceAdmin)
admin.site.register(EventType)
admin.site.register(EventImages, EventImagesAdmin)

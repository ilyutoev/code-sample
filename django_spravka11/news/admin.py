from django.contrib import admin
from news.models import News, Category

class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date')
    
    class Media:
        js = [
        '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
        '/static/grappelli/tinymce_setup/tinymce_setup.js',
        ]

admin.site.register(News,NewsAdmin)
admin.site.register(Category)
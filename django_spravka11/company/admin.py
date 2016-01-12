from django.contrib import admin
from company.models import Category, Company, Address, Phone, City, CompanyImage, CompanyNews, CompanyService, Timetable, CompanyPage
from mptt.admin import MPTTModelAdmin

from import_export.admin import ImportExportModelAdmin
from import_export import resources


class AddressInline(admin.StackedInline):
    model = Address
    extra = 1

class PhoneInline(admin.StackedInline):
    model = Phone
    extra = 1

class CompanyImageInline(admin.StackedInline):
    model = CompanyImage
    extra = 1

class CompanyAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    inlines = [AddressInline, CompanyImageInline]
    search_fields = ['name']
    class Media:
        js = [
        '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
        '/static/grappelli/tinymce_setup/tinymce_setup.js',
        ]


class AddressAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    inlines = [PhoneInline]
    list_display = ['company', 'address', 'city']
    filter_horizontal = ('category', )

class CompanyNewsAdmin(admin.ModelAdmin):
    raw_id_fields = ('company',)
    autocomplete_lookup_fields = {
        'fk': ['company'],
    }
    class Media:
        js = [
        '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
        '/static/grappelli/tinymce_setup/tinymce_setup.js',
        ]

class CompanyPageAdmin(admin.ModelAdmin):
    raw_id_fields = ('company',)
    autocomplete_lookup_fields = {
        'fk': ['company'],
    }
    class Media:
        js = [
        '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
        '/static/grappelli/tinymce_setup/tinymce_setup.js',
        ]

class CategoryAdmin(MPTTModelAdmin):
    class Media:
        js = [
        '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
        '/static/grappelli/tinymce_setup/tinymce_setup.js',
        ]

admin.site.register(Category, CategoryAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Phone, ImportExportModelAdmin)
admin.site.register(City)
admin.site.register(CompanyNews, CompanyNewsAdmin)
admin.site.register(CompanyService, CompanyNewsAdmin)
admin.site.register(Timetable, ImportExportModelAdmin)
admin.site.register(CompanyPage, CompanyPageAdmin)
from django import forms


class UploadFileImportForm(forms.Form):
    importfile = forms.FileField(label='Файл с данными для импорта')
import datetime
from haystack import indexes
from company.models import Address


class AddressIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    city = indexes.CharField(model_attr='city__name')
    company = indexes.CharField(model_attr='company__pk')

    suggestions = indexes.FacetCharField()

    def prepare(self, obj):
        prepared_data = super(AddressIndex, self).prepare(obj)
        prepared_data['suggestions'] = prepared_data['text']
        return prepared_data

    def get_model(self):
        return Address
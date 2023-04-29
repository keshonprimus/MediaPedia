import django_filters

from .models import *

class SearchFilter(django_filters.FilterSet):
    class Meta:
        model = Products
        fields = '__all__'

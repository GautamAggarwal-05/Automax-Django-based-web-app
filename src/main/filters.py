import django_filters

from .models import Listing


class ListingsFilter(django_filters.FilterSet):
    class Meta:
        model = Listing
        # icontains for case-insensitive search, exact for exact match, lt for less than
        fields = {'brand':['exact'],'transmission':['exact'],'mileage':{'lt'},'model':{'icontains'}} 
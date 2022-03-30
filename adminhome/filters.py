import django_filters
from .models import  ParkingCategory, ParkingSpot

class ParkingCatergoryFilter(django_filters.FilterSet):
    # name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = ParkingCategory
        fields = ('is_active',)

class ParkingSpotFilter(django_filters.FilterSet):

    class Meta:
        model = ParkingSpot
        fields = ('is_active', 'parking_category_id',)
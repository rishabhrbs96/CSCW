import django_filters
from .models import  ParkingCategory, ParkingSpot, Booking

class ParkingCatergoryFilter(django_filters.FilterSet):
    # name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = ParkingCategory
        fields = ('is_active',)

class ParkingSpotFilter(django_filters.FilterSet):

    class Meta:
        model = ParkingSpot
        fields = ('is_active', 'parking_category_id',)

class BookingFilter(django_filters.FilterSet):

    class Meta:
        model = Booking
        fields = ('parking_spot_id', 'start_time', 'end_time', 'lease_is_signed_by_user', 'state',)

class PreviousBookingFilter(django_filters.FilterSet):

    class Meta:
        model = Booking
        fields = ('parking_spot_id', 'start_time', 'end_time', 'state',)

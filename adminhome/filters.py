import django_filters
from .models import  ParkingCategory, ParkingSpot, Booking, Vehicle
from .forms import DatePickerInput

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
        fields = ('parking_spot_id', 'lease_is_signed_by_user', 'state', 'vehicle_id__user_id',)
        # fields = {
        #     'parking_spot_id': ['exact'], 
        #     'start_time': ['gte'], 
        #     'end_time': ['lte'], 
        #     'lease_is_signed_by_user': ['exact'], 
        #     'state': ['exact'],
        # }
        # widgets = {
        #     'start_time': DatePickerInput,
        # }

class PreviousAndCurrentBookingFilter(django_filters.FilterSet):

    class Meta:
        model = Booking
        fields = ('parking_spot_id', 'state', 'vehicle_id__user_id',)

class UnverifiedVehiclesFilter(django_filters.FilterSet):

    class Meta:
        model = Vehicle
        fields = ('user_id',)

from email.policy import default
import uuid

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

#####################################################################################
#                                       ENUMS                                       #
#####################################################################################
class BookingStates(models.TextChoices):
    NEW = 'new', _('New Booking')
    PENDING_APPROVAL = 'pending', _('Pending Approval')
    PENDING_LEASE = 'pending_lease', _('Pending Lease')
    REJECTED = 'rejected', _('Rejected Booking')
    APPROVED = 'approved', _('Approved Booking')
    CANCELED_BEFORE_LEASE = 'canceled_before_lease', _('Canceled Before Lease')
    CANCELED = 'canceled', _('Canceled Booking')
    PAID = 'paid', _('Paid Booking')
    UNPAID = 'unpaid', _('Unpaid Booking')

class PaymentStatus(models.TextChoices):
    PAID = 'paid', _('Paid')
    UNPAID = 'unpaid', _('Unpaid')

class PaymentMethod(models.TextChoices):
    CASH = 'cash', _('Cash Payment')
    CARD = 'card', _('Card Payment')
    ONLINE = 'online', _('Online Payment')

class ViewBookings(models.TextChoices):
    UPCOMING_BOOKINGS = 'upcoming_bookings', _('Upcoming Bookings')
    PREVIOUS_BOOKINGS = 'previous_bookings', _('Previous Bookings')
    CURRENT_BOOKINGS = 'current_bookings', _('Current Bookings')

#####################################################################################
#                                      MODELS                                       #
#####################################################################################
class ParkingCategory(models.Model):
    name = models.CharField(max_length=200, unique=True)
    size = models.DecimalField(max_digits=1000, decimal_places=2)
    daily_rate = models.DecimalField(max_digits=1000, decimal_places=2)
    weekly_rate = models.DecimalField(max_digits=1000, decimal_places=2)
    monthly_rate = models.DecimalField(max_digits=1000, decimal_places=2)
    utility_conversion_rate = models.DecimalField(max_digits=1000, decimal_places=2)
    is_active = models.BooleanField()
    cancellation_penalty = models.DecimalField(max_digits=1000, decimal_places=2)
    cancellation_time_window = models.IntegerField()

    def __str__(self):
        return self.name

class ParkingSpot(models.Model):
    name = models.CharField(max_length=200, unique=True)
    is_active = models.BooleanField()
    parking_category_id = models.ForeignKey(ParkingCategory, on_delete=models.CASCADE, related_name="parking_spot")

    def __str__(self):
        return self.name

class Vehicle(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    build = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    insurance_doc = models.FileField(upload_to='insurance/')
    is_verified = models.BooleanField(default=False)
    insurance_expiry_date = models.DateTimeField(null=True)

    def __str__(self):
        return self.name

class Payment(models.Model):
    status = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.UNPAID)
    method = models.CharField(max_length=20, choices=PaymentMethod.choices, default=PaymentMethod.CASH)
    time = models.DateTimeField(auto_now_add=False)

class Booking(models.Model):
    vehicle_id = models.ForeignKey(Vehicle, on_delete=models.PROTECT, related_name="booking", default=None, null=True)
    pc_id = models.ForeignKey(ParkingCategory, on_delete=models.PROTECT, related_name="booking", default=None, null=True)
    parking_spot_id = models.ForeignKey(ParkingSpot, on_delete=models.PROTECT, related_name="booking", default=None, null=True)
    start_time = models.DateTimeField(auto_now_add=False)
    end_time = models.DateTimeField(auto_now_add=False)
    state = models.CharField(max_length=30, choices=BookingStates.choices, default=BookingStates.NEW)
    lease_doc_url = models.CharField(max_length=100)
    lease_is_signed_by_user = models.BooleanField()
    admin_comments = models.CharField(max_length=20)
    
class BillDetail(models.Model):
    bill_date = models.DateTimeField(auto_now_add=False)
    reservation_cost = models.DecimalField(max_digits=1000, decimal_places=2)
    init_meter_reading = models.IntegerField()
    end_meter_reading = models.IntegerField()
    meter_rate = models.DecimalField(max_digits=1000, decimal_places=2)
    utility_cost = models.DecimalField(max_digits=1000, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=1000, decimal_places=2)
    unpaid_amount = models.DecimalField(max_digits=1000, decimal_places=2)
    payment_id = models.ForeignKey(Payment, on_delete=models.PROTECT, related_name="bills")
    misc_charges = models.DecimalField(max_digits=1000, decimal_places=2)
    booking_id = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="bills")
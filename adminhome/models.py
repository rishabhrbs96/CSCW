from email.policy import default
import uuid

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from .enums import BookingStates, PaymentMethod

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
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    build = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    insurance_doc = models.FileField(upload_to='insurance/')
    is_verified = models.BooleanField(default=False)
    insurance_expiry_date = models.DateTimeField(null=True)

    def __str__(self):
        return self.name

class Booking(models.Model):
    vehicle_id = models.ForeignKey(Vehicle, on_delete=models.PROTECT, related_name="booking", default=None, null=True)
    pc_id = models.ForeignKey(ParkingCategory, on_delete=models.PROTECT, related_name="booking", default=None, null=True)
    parking_spot_id = models.ForeignKey(ParkingSpot, on_delete=models.PROTECT, related_name="booking", default=None, null=True)
    start_time = models.DateTimeField(auto_now_add=False)
    end_time = models.DateTimeField(auto_now_add=False)
    creation_time = models.DateTimeField(auto_now_add=True)
    lease_sign_time = models.DateTimeField(auto_now_add=False, null=True)
    last_modified_time = models.DateTimeField(auto_now=True)
    last_modified_userid = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    state = models.CharField(max_length=30, choices=BookingStates.choices, default=BookingStates.NEW)
    lease_doc_url = models.CharField(max_length=100)
    lease_is_signed_by_user = models.BooleanField()
    
    admin_comments = models.CharField(max_length=20)
    
class BillDetail(models.Model):
    bill_date = models.DateTimeField(auto_now_add=False)
    reservation_cost = models.DecimalField(max_digits=1000, decimal_places=2, default=0)
    init_meter_reading = models.IntegerField(default=0)
    end_meter_reading = models.IntegerField(default=0)
    meter_rate = models.DecimalField(max_digits=1000, decimal_places=2, default=0)
    utility_cost = models.DecimalField(max_digits=1000, decimal_places=2, default=0)
    paid_amount = models.DecimalField(max_digits=1000, decimal_places=2)
    unpaid_amount = models.DecimalField(max_digits=1000, decimal_places=2)
    misc_charges = models.DecimalField(max_digits=1000, decimal_places=2, default=0)
    comments = models.TextField(null=True)
    booking_id = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="bills")

class Payment(models.Model):
    # status = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.UNPAID)
    method = models.CharField(max_length=20, choices=PaymentMethod.choices, default=PaymentMethod.CASH)
    time = models.DateTimeField(auto_now_add=False)
    bill = models.ForeignKey(BillDetail, on_delete=models.CASCADE, related_name="payments")
    amount = models.DecimalField(max_digits=1000, decimal_places=2, default=0)
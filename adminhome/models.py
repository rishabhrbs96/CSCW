from django.db import models


# Create your models here.

class ParkingCategory(models.Model):
    name = models.CharField(max_length=200, unique=True)
    size = models.DecimalField(decimal_places=2)
    rent_daily_rate = models.DecimalField(decimal_places=2)
    rent_weekly_rate = models.DecimalField(decimal_places=2)
    rent_monthly_rate = models.DecimalField(decimal_places=2)
    utility_rate = models.DecimalField(decimal_places=2)
    is_active = models.BooleanField()
    min_time_window = models.IntegerField()
    cancellation_charges = models.DecimalField(decimal_places=2)
    cancellation_policy = models.IntegerField()


class ParkingSpot(models.Model):
    name = models.CharField(max_lenth=200, unique=True)
    is_active = models.BooleanField()
    parking_category_id = models.ForeignKey(ParkingCategory, on_delete=models.CASCADE, related_name="parking_spot")


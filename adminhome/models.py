from django.db import models

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

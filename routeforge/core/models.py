from django.db import models

# Create your models herefrom django.db import models


class Courier(models.Model):
    name = models.CharField(max_length=100)
    current_lat = models.FloatField(null=True, blank=True)
    current_lng = models.FloatField(null=True, blank=True)
    is_available = models.BooleanField(default=True)
    avg_speed_kmh = models.FloatField(default=30.0)

    def __str__(self):
        return self.name

class Delivery(models.Model):
    pickup_lat = models.FloatField()
    pickup_lng = models.FloatField()
    drop_lat = models.FloatField()
    drop_lng = models.FloatField()

    status = models.CharField(
        max_length=20,
        default="pending"
    )

    assigned_courier = models.ForeignKey(
        Courier,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Delivery #{self.id} ({self.status})"

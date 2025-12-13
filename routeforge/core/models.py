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

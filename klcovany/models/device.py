from django.db import models


class Device(models.Model):
    name = models.CharField(max_length=128)
    external_id = models.CharField(max_length=50)
    status = models.CharField(max_length=4)
    consumption = models.IntegerField(default=0)
    priority = models.IntegerField(default=1)
    is_selected = models.BooleanField(default=False)
    plant = models.ForeignKey("Plant", on_delete=models.CASCADE, related_name="devices")

    def __str__(self):
        return self.name

from datetime import datetime, timezone
from django.db import models
from klcovany.src.computer import Computer

from klcovany.src.sonoff import Sonoff

# Create your models here.


class Plant(models.Model):
    code = models.CharField(max_length=128)
    meter_id = models.CharField(max_length=128)
    energy_surplus = models.IntegerField()
    last_refresh = models.DateTimeField()

    def refresh(self):
        delta = datetime.now(timezone.utc) - self.last_refresh
        if delta.seconds > 290:
            sonoff = Sonoff(self.devices.all(), self)

            computer = Computer(self.code, self.meter_id)
            energy_surplus = computer.refresh_energy_surplus(sonoff)

            self.energy_surplus = energy_surplus
            self.last_refresh = datetime.now(timezone.utc)

            self.save()

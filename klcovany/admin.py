from django.contrib import admin

from .models.plant import Plant
from .models.device import Device
from .models.log import Log
# Register your models here.

admin.site.register(Device)
admin.site.register(Plant)
admin.site.register(Log)

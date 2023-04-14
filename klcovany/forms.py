from django.forms import ModelForm
from .models.device import Device


class DeviceForm(ModelForm):
    class Meta:
        model = Device
        fields = ["is_selected", "consumption", "priority"]

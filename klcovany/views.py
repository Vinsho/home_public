from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views import View

from klcovany.forms import DeviceForm
from .models.plant import Plant
from .models.device import Device

# Create your views here.


class PlantView(LoginRequiredMixin, View):
    template = "klcovany/klcovany.html"

    def get(self, request):
        plant = Plant.objects.all()[0]  # TODO add support for more
        return render(request, self.template, {'plant': plant, 'priority_range': range(1, len(plant.devices.all()) + 1)})

    def post(self, request):
        device = get_object_or_404(Device, pk=request.POST.get('device_id'))
        device_form = DeviceForm(request.POST, instance=device, initial={"is_selected": False})

        if device_form.is_valid():
            device_form.save()
        else:
            print(device_form.errors)

        return redirect(request.META['HTTP_REFERER'])


class HomeView(View):
    template = "home.html"

    def get(self, request):
        return render(request, self.template)


class LoginView(View):
    template = "klcovany/login.html"

    def get(self, request):
        return render(request, self.template)

import os
import hmac
import hashlib
import base64
import json
import requests
from klcovany.models.log import Log
from klcovany.models.device import Device


class Sonoff:
    def __init__(self, devices: list[Device], plant) -> None:
        self.base = "https://eu-apia.coolkit.cc/v2"
        self.__app_secret = os.environ['SONOFF_APP_SECRET'].encode('UTF-8')
        self.__x_ck_appid = os.environ['SONOFF_APP_ID']

        self.email = os.environ["EWELINK_API_USER"]
        self.password = os.environ["EWELINK_API_PASSWORD"]

        self.client = self.login()
        self.devices = devices
        self.plant = plant

    def login(self):
        body = {"email": self.email, "password": self.password, "countryCode": "+421"}

        hex_dig = hmac.new(
            self.__app_secret,
            str.encode(json.dumps(body)),
            digestmod=hashlib.sha256).digest()

        sign = base64.b64encode(hex_dig).decode()

        headers = {
            'Authorization': 'Sign ' + sign,
            'Content-Type': 'application/json',
            "X-CK-Appid": self.__x_ck_appid
        }

        return requests.post(f'{self.base}/user/login',
                             headers=headers, json=body).json()['data']

    @property
    def headers(self):
        return {
            'Authorization': 'Bearer ' + self.client['at'],
            'Content-Type': 'application/json',
            "X-CK-Nonce": 'lopenumo'
        }

    @property
    def selected_devices(self):
        return [device for device in self.devices if device.is_selected]

    def refresh_devices(self):
        try:
            for device in self.get_devices():
                device_object, _ = Device.objects.update_or_create(
                    external_id=device['deviceid'],
                    plant_id=self.plant.id,
                    defaults={
                        'name': device['name'],
                        'status': device['params']['switch']
                    }
                )
                device_object.save()

        except Exception as e:
            Log(message=f"Unable to fetch devices: {e}", plant_id=self.plant.id).save()

            # In case we are unable to refresh devices, turn them off just in case
            self.switch_off_all_devices()
            return False

        return True

    def switch_device(self, device: Device, switch: str):
        if device.status == switch:
            return

        url = self.base + '/device/thing/status'

        body = {
            "type": 1,
            "id": device.external_id,
            "params": {
                "switch": switch
            }
        }

        requests.post(url, headers=self.headers, json=body)
        device.status = switch
        device.save()

        Log(message=f"Turning device {device.name} **{switch.upper()}**", plant_id=self.plant.id).save()

    def get_consumption_of_on_devices(self):
        return sum(device.consumption for device in self.devices if device.status == "on")

    def switch_devices_on(self, energy_surplus: int):
        for device in sorted(self.selected_devices, key=lambda x: x.priority):
            if device.consumption < energy_surplus and device.status != "on":
                self.switch_device(device, "on")
                energy_surplus -= device.consumption

    def switch_devices_off(self, energy_surplus: int):
        energy_surplus += self.get_consumption_of_on_devices()

        for device in sorted(self.devices, key=lambda x: x.priority):
            if device.status == "off":
                continue

            if device.consumption > energy_surplus:
                self.switch_device(device, "off")
            else:
                energy_surplus -= device.consumption

    def switch_off_all_devices(self):
        Log(message="Forcing turn off", plant_id=self.plant.id).save()

        for device in self.devices:
            self.switch_device(device, "off")

    def resolve_energy_surplus(self, energy_surplus: int):
        if not self.refresh_devices():
            return

        if energy_surplus > 0:
            self.switch_devices_on(energy_surplus)
        elif energy_surplus < 0:
            self.switch_devices_off(energy_surplus)

    def get_at(self, link):
        return requests.get(link, headers=self.headers).json()['data']

    def get_devices(self):
        url = f"{self.base}/device/thing"

        devices_data = self.get_at(url)

        return [thing['itemData'] for thing in devices_data['thingList']]

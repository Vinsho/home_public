import os
from klcovany.models.log import Log
from klcovany.src.fusion_solar import Client
from klcovany.src.sonoff import Sonoff


class Computer:
    def __init__(self, plant_code, meter_id) -> None:
        self.client = Client(
            user_name=os.environ["HUAWEI_API_USER"], system_code=os.environ["HUAWEI_API_PASSWORD"])
        self.meter_name = "Meter-1"
        self.meter_dev_type_id = 47

        self.plant_code = plant_code
        self.meter_id = meter_id

    def validate(self, response):
        if not response['success']:
            raise Exception(response['data'])

        return response

    def get_meter_data(self):
        return self.validate(self.client.get_dev_kpi_real(dev_id=self.meter_id, dev_type_id=self.meter_dev_type_id))

    def refresh_energy_surplus(self, sonoff: Sonoff):
        try:
            meter_data = self.get_meter_data()['data']
            energy_surplus = int(meter_data[0]['dataItemMap']['active_power'])
            Log(message=f"Refreshed energy surplus: {energy_surplus}", plant_id=sonoff.plant.id).save()
        except Exception as e:
            Log(message=f"Unable to refresh energy surplus: {e}", plant_id=sonoff.plant.id).save()

            energy_surplus = 0

        sonoff.resolve_energy_surplus(energy_surplus)

        return energy_surplus

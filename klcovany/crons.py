from klcovany.models.log import Log
from klcovany.models.plant import Plant


def refresh_plant():
    try:
        plant = Plant.objects.first()

        plant.refresh()
    except Exception as e:
        Log(message=f"Refresh failed {e}", plant_id=plant.id)

from django.db import models


class Log(models.Model):
    message = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)
    plant = models.ForeignKey("Plant", on_delete=models.CASCADE, related_name="logs")

    def __str__(self):
        return f'[{self.datetime.strftime("%d.%m %H:%M:%S")}] {self.message}'

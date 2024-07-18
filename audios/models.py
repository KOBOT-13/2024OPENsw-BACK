from django.db import models
from django.utils import timezone

class AudioText(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateTimeField(default=timezone.now, editable=False)
    text = models.TextField()

    def __str__(self):
        return str(self.date)
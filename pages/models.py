from django.db import models

class AudioText(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateTimeField(max_length=12, editable=False)
    text = models.TextField()

    def __str__(self):
        return self.date

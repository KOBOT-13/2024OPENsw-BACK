from django.db import models

class Video(models.Model):
    custom_id = models.CharField(max_length=12, primary_key=True, editable=False, unique=True)
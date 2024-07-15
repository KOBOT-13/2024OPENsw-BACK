from django.db import models

class Page(models.Model):
    date = models.DateField(auto_now_add=True, verbose_name="date")

    def __str__(self):
        return self.date
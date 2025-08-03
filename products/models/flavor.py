from django.db import models


class Flavor(models.Model):
    name = models.CharField(max_length=32)

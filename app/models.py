from django.db import models


class page(models.Model):
    name =models.CharField(max_length=15)
    
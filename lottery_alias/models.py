from django.contrib.postgres.fields import ArrayField
from django.db import models

from lottery.common import *


class Alias(models.Model):
    id = models.AutoField(primary_key=True)
    list = ArrayField(models.CharField(max_length=64))

    def __str__(self):
        return str(self.id)

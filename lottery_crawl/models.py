from django.db import models


class Alias(models.Model):
    id = models.AutoField(primary_key=True)
    a = models.CharField(max_length=36)
    b = models.CharField(max_length=36)

    def __str__(self):
        return str(self.id) + ": (" + str(self.a) + "," + str(self.b) + ")"

from django.db import models


class Odd(models.Model):
    home = models.FloatField()
    draw = models.FloatField()
    away = models.FloatField()

    def __str__(self):
        return "(" + str(self.home) + ", " + str(self.draw) + ", " + str(self.away) + ")"


class Market(models.Model):
    src = models.CharField(max_length=5, choices=(
        ('5C', '500'),
        ('HK-CH', 'HKJC(Chinese)'),
        ('HK-EN', 'HKJC(English)'),
        ('MS', 'MacauSlot'),
        ('BF', 'Betfair')
    ))
    market = models.CharField(max_length=16)
    update = models.DateTimeField(null=True)
    t = models.DateTimeField(null=True)
    home = models.CharField(max_length=64, null=True)
    away = models.CharField(max_length=64, null=True)
    odd = models.ForeignKey(Odd, null=True)

    class Meta:
        unique_together = ("src", "market")

    def __str__(self):
        return str(self.id)

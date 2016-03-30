from django.db import models


class Odd(models.Model):
    home = models.FloatField()
    draw = models.FloatField()
    away = models.FloatField()

    def __str__(self):
        return "(" + str(self.home) + ", " + str(self.draw) + ", " + str(self.away) + ")"


class Market(models.Model):
    src = models.CharField(max_length=2, choices=(
        ('5C', '500'),
        ('HK', 'HKJC'),
        ('MS', 'MacauSlot'),
        ('BF', 'Betfair')
    ))
    market = models.CharField(max_length=16)
    update = models.DateTimeField()
    t = models.DateTimeField()
    home = models.CharField(max_length=64)
    away = models.CharField(max_length=64)
    odd = models.ForeignKey(Odd)

    class Meta:
        unique_together = ("src", "market")

    def __str__(self):
        return str(self.id)

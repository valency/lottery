from django.db import models


# class AsianOdd(models.Model):
#     team = models.CharField(max_length=1, choices=(
#         ('H', 'Home'),
#         ('A', 'Away')
#     ))
#     mode = models.CharField(max_length=16)
#     home = models.FloatField()
#     away = models.FloatField()
#
#     def __str__(self):
#         return str(self.team) + " " + str(self.mode) + ": (" + str(self.home) + ", " + str(self.away) + ")"
#
#
# class AsianMarket(models.Model):
#     id = models.AutoField(primary_key=True)
#     market = models.CharField(max_length=16)
#     home = models.CharField(max_length=64)
#     away = models.CharField(max_length=64)
#     odd = models.ForeignKey(Odd)
#
#     def __str__(self):
#         return str(self.id)

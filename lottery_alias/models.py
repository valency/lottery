from django.db import models


class Alias(models.Model):
    id = models.AutoField(primary_key=True)
    zh_cn = models.CharField(max_length=64)
    zh_tw = models.CharField(max_length=64)
    en_hk = models.CharField(max_length=64)
    en_gb = models.CharField(max_length=64)

    class Meta:
        unique_together = ("zh_cn", "zh_tw", "en_hk", "en_gb")

    def __str__(self):
        return str(self.id)

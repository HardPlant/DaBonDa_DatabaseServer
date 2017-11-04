from django.db import models
import datetime

# Create your models here.
class SoundData(models.Model):
    dB = models.FloatField(default = -1)
    time = models.DateTimeField(str(datetime.datetime.now()))
    photoId = models.CharField(max_length=200)
    hash = models.BinaryField(max_length=256, default='')

    def __str__(self):
        return "SoundData at" + str(self.time) \
               +', dB:' + str(self.dB)
from django.db import models
from stdimage.models import StdImageField
from django.utils import timezone


class StudentCard(models.Model):
    id = models.CharField(max_length=7, primary_key=True)
    name = models.CharField(max_length=64)
    balance = models.IntegerField()
    # icon = models.ImageField(upload_to='images/')
    icon = StdImageField(upload_to='images/', variations={'for_comparing': (350, 350), 'thumbnail': (500, 500)})
    bio = models.CharField(max_length=128)


class ICCharger(models.Model):
    id = models.IntegerField(primary_key=True)
    last_charge_date = models.DateTimeField(default=timezone.now)


class TopUpHistory(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.CharField(max_length=7)
    date = models.DateTimeField(default=timezone.now)
    balance = models.IntegerField()
    top_up_money = models.IntegerField()

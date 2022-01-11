# Create your models here.
from __future__ import unicode_literals
from django.db import models

# Create your models here.
class AccessToken(models.Model):
    token = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        get_latest_by = 'created_at'

    def __str__(self):
	    return self.token
class Mat(models.Model):
    sacco_name = models.CharField(max_length=30)
    terminus = models.CharField(max_length=30)
    route = models.CharField(max_length=30)
    nos = models.DecimalField(decimal_places=0, max_digits=2)
    rem = models.DecimalField(decimal_places=0, max_digits=2)
    fare_price = models.DecimalField(decimal_places=2, max_digits=6)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return self.sacco_name


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField()
    name = models.CharField(max_length=30)
    password = models.CharField(max_length=30)

    def __str__(self):
        return self.email


class Booking(models.Model):
    BOOKED = 'B'
    CANCELLED = 'C'

    TICKET_STATUSES = ((BOOKED, 'Booked'),
                       (CANCELLED, 'Cancelled'),)
    email = models.EmailField()
    name = models.CharField(max_length=30)
    userid =models.DecimalField(decimal_places=0, max_digits=2)
    mat_id=models.DecimalField(decimal_places=0, max_digits=2)
    sacco_name = models.CharField(max_length=30)
    terminus = models.CharField(max_length=30)
    route = models.CharField(max_length=30)
    nos = models.DecimalField(decimal_places=0, max_digits=2)
    fare_price = models.DecimalField(decimal_places=2, max_digits=6)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(choices=TICKET_STATUSES, default=BOOKED, max_length=255)

    def __str__(self):
        return self.status

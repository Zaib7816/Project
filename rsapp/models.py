from django.db import models

# Create your models here.


class University(models.Model):
    name = models.CharField(max_length=300, default="")
    image = models.ImageField(upload_to='img', null=True, blank=True)
    city_id = models.CharField(max_length=100, default="")
    address = models.CharField(max_length=300, default="")
    city = models.CharField(max_length=300, default="")
    description = models.CharField(max_length=500, default="")
    low = models.CharField(max_length=300, default="")
    log_avg = models.CharField(max_length=300, default="")
    medium = models.CharField(max_length=300, default="")
    medium_avg = models.CharField(max_length=300, default="")
    high = models.CharField(max_length=300, default="")
    high_avg = models.CharField(max_length=300, default="")
    cgpa = models.CharField(max_length=300, default="")
    uni_link = models.CharField(max_length=300, default="")

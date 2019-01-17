from django.db import models
#from django.utils import timezone


class Region(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Substation(models.Model):
    name = models.CharField(max_length=50)
    short_name = models.CharField(max_length=5)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self):
        return self.short_name


class Transformer(models.Model):
    name = models.CharField(max_length=10, default='TR-01')
    substation = models.ForeignKey(Substation, on_delete=models.CASCADE)
    serial_number = models.CharField(max_length=20)
    install_date = models.DateField()
    voltage = models.FloatField(default=138.0)
    nominal_power = models.FloatField(default=12.5)
    class_temperature = models.IntegerField(default=55)
    path_name = models.CharField(max_length=20)

    #def __init__(self):
        #self.path_name = self.substation + self.name

    def __str__(self):
        return self.path_name


from django.db import models

# Create your models here.
class Grades(models.Model):
    name = models.CharField(max_length=255)
    grade1 = models.DecimalField(max_digits=3, decimal_places=1)
    grade2 = models.DecimalField(max_digits=3, decimal_places=1)
    grade3 = models.DecimalField(max_digits=3, decimal_places=1)



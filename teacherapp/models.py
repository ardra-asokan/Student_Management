from django.db import models

# Create your models here.
class Attendance(models.Model):
    student = models.CharField(max_length=100,blank=True,null=True)
    subject = models.CharField(max_length=100,blank=True,null=True)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=(('Present','Present'),('Absent','Absent')))

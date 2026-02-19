from django.db import models

# Create your models here.
class LeaveApplicationDb(models.Model):
    student_name = models.CharField(max_length=100)
    subject = models.CharField(max_length=200)
    from_date = models.DateField()
    to_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20,default="Pending")
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.student_name
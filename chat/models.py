from django.db import models
from Adminapp.models import StudentDb, TeacherDb

# Create your models here.
class ChatMessageDb(models.Model):
    sender_teacher = models.ForeignKey(
        TeacherDb,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    sender_student = models.ForeignKey(
        StudentDb,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.sender}: {self.message[:30]}"

from django.db import models
from Adminapp.models import StudentDb, AssignedSubjectDb,SubjectDb,TeacherDb

class AttendanceDb(models.Model):
    student = models.ForeignKey(StudentDb, on_delete=models.CASCADE)
    subject = models.ForeignKey(SubjectDb, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10,choices=[('Present', 'Present'), ('Absent', 'Absent')])

    def __str__(self):
        return f"{self.student.name} – {self.subject.subject_name} – {self.status}"

class MarksDb(models.Model):
    student = models.ForeignKey(StudentDb,on_delete=models.CASCADE,
        related_name="student_marks")
    subject = models.ForeignKey(SubjectDb,on_delete=models.CASCADE,
        related_name="subject_marks")

    exam_type = models.CharField(max_length=50)
    marks = models.IntegerField()
    date = models.DateField()

    def __str__(self):
        return f"{self.student.name} - {self.subject.subject_name} - {self.exam_type}"

class AssignmentDb(models.Model):
    teacher = models.ForeignKey(TeacherDb, on_delete=models.CASCADE)
    subject = models.ForeignKey(SubjectDb, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    deadline = models.DateField()
    assignment_file = models.FileField(upload_to="assignments/")
    created_at = models.DateTimeField(auto_now_add=True)

class AssignmentSubmissionDb(models.Model):
    assignment = models.ForeignKey(AssignmentDb, on_delete=models.CASCADE)
    student = models.ForeignKey(StudentDb, on_delete=models.CASCADE)
    file = models.FileField(upload_to="submitted_assignments/")
    submitted_at = models.DateTimeField(auto_now_add=True)
    marks = models.IntegerField(null=True, blank=True)

class StudyMaterialDb(models.Model):
    teacher = models.ForeignKey(TeacherDb, on_delete=models.CASCADE)
    subject = models.ForeignKey(SubjectDb, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    material_file = models.FileField(upload_to='study_materials/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
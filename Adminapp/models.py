from django.db import models

# Create your models here.
class StudentDb(models.Model):
    name = models.CharField(max_length=100,null=True,blank=True)
    roll_no = models.CharField(max_length=100,null=True,blank=True)
    dob = models.DateField()
    gender = models.CharField(max_length=100,null=True,blank=True)
    email = models.EmailField(max_length=100,null=True,blank=True)
    phone = models.CharField(max_length=100,null=True,blank=True)
    department = models.CharField(max_length=100,null=True,blank=True)
    semester = models.CharField(max_length=100,null=True,blank=True)
    batch = models.CharField(max_length=100,null=True,blank=True)
    username = models.CharField(max_length=100,null=True,blank=True)
    password = models.CharField(max_length=100,null=True,blank=True)
    address = models.TextField()
    profile_photo = models.ImageField(upload_to='User Profiles', null=True, blank=True)

class TeacherDb(models.Model):
    name = models.CharField(max_length=100,null=True,blank=True)
    employee_id = models.CharField(max_length=50, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(max_length=100,null=True,blank=True)
    phone = models.CharField(max_length=100,null=True,blank=True)
    department = models.CharField(max_length=100,null=True,blank=True)
    qualification = models.CharField(max_length=100,null=True,blank=True)
    experience = models.CharField(max_length=100,null=True,blank=True)
    username = models.CharField(max_length=100,null=True,blank=True)
    password = models.CharField(max_length=100,null=True,blank=True)
    address = models.TextField()
    profile_photo = models.ImageField(upload_to='User Profiles', null=True, blank=True)

    def __str__(self):
        return self.name

class SubjectDb(models.Model):
    subject_name = models.CharField(max_length=100,null=True,blank=True)
    subject_code = models.CharField(max_length=100,null=True,blank=True)
    department = models.CharField(max_length=100,null=True,blank=True)
    semester = models.CharField(max_length=100,null=True,blank=True)
    teacher = models.ForeignKey(TeacherDb, on_delete=models.SET_NULL, null=True, blank=True)

class AssignedSubjectDb(models.Model):
    teacher = models.CharField(max_length=100,null=True,blank=True)
    subject = models.ForeignKey(SubjectDb, on_delete=models.CASCADE)
    class_name = models.CharField(max_length=100,null=True,blank=True)
    semester = models.CharField(max_length=100,null=True,blank=True)



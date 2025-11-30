from django.contrib import admin
from Adminapp.models import StudentDb,TeacherDb,SubjectDb,AssignedSubjectDb

# Register your models here.

admin.site.register(StudentDb)
admin.site.register(TeacherDb)
admin.site.register(SubjectDb)
admin.site.register(AssignedSubjectDb)
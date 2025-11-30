from django.shortcuts import render,redirect
from Adminapp.models import SubjectDb

# Create your views here.
def student_page(request):
    return render(request, "Student_index.html")
def student_profile(request):
    return render(request, 'StudentProfile.html')
def student_subjects(request):
    return render(request, 'Student_Subjects.html')
def student_attendance(request):
    return render(request, 'Student_attendance.html')
def student_timetable(request):
    return render(request, 'Student_timetable.html')
def student_results(request):
    return render(request, 'Student_results.html')
def student_assignments(request):
    return render(request, 'Student_assignments.html')
def student_notifications(request):
    return render(request, 'Student_notifications.html')
#
# def student_support(request):
#     return render(request, 'student/support.html')
#

def student_dashboard(request):
    if 'Name' in request.session:
        return render(request, 'student_index.html')
    else:
        return redirect('student_log_in')


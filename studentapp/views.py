from django.shortcuts import render,redirect
from Adminapp.models import SubjectDb,StudentDb
from teacherapp.models import AttendanceDb,MarksDb,AssignmentSubmissionDb
from django.db.models import Count, Q

# Create your views here.
def student_page(request):
    return render(request, "Student_index.html")
def student_profile(request):
    student_id = request.session.get('student_id')

    if not student_id:
        return redirect('student_log_in')

    student = StudentDb.objects.get(id=student_id)

    return render(request, 'View_Student_Profile.html', {
        'student': student
    })


def edit_profile(request):
    student_id = request.session.get('student_id')

    if not student_id:
        return redirect('student_log_in')

    student = StudentDb.objects.get(id=student_id)

    if request.method == "POST":
        student.email = request.POST.get('email')
        student.phone = request.POST.get('phone')
        student.address = request.POST.get('address')

        if 'photo' in request.FILES:
            student.photo = request.FILES['photo']

        student.save()
        return redirect('student_profile')  # back to view profile

    return render(request, 'Edit_Student_Profile.html', {
        'student': student
    })
def view_student_subjects(request):
    student_id = request.session.get('student_id')

    if not student_id:
        return redirect('student_log_in')

    student = StudentDb.objects.get(id=student_id)

    # example: subjects assigned to student's class & semester
    subjects = SubjectDb.objects.filter(
        department=student.department,
        semester=student.semester
    )

    return render(request, 'View_Student_Subjects.html', {
        'subjects': subjects
    })
def subject_details(request, subject_id):
    student_id = request.session.get('student_id')

    if not student_id:
        return redirect('student_log_in')

    subject = SubjectDb.objects.get(id=subject_id)

    return render(request, 'Subject_Details.html', {
        'subject': subject
    })


def student_attendance(request):

    student_name = request.session.get('student_name')

    if not student_name:
        return redirect('student_log_in')

    attendance = (
        AttendanceDb.objects
        .filter(student=student_name)
        .values('subject')
        .annotate(
            total=Count('id'),
            present=Count('id', filter=Q(status='Present'))
        )
    )

    for a in attendance:
        a['percent'] = round(
            (a['present'] / a['total']) * 100, 2
        ) if a['total'] > 0 else 0

    return render(request, 'Student_attendance.html', {
        'attendance': attendance
    })

def student_timetable(request):
    return render(request, 'Student_timetable.html')



def student_assignments(request):
    student_name = request.session.get('student_name')

    if not student_name:
        return redirect('student_log_in')

    student = StudentDb.objects.get(name=student_name)

    assignments = AssignmentDb.objects.filter(
        class_name=student.class_name,
        semester=student.semester
    )

    return render(request, 'Student_assignments.html', {
        'assignments': assignments
    })
def student_internal_marks(request):
    student_name = request.session.get('student_name')

    if not student_name:
        return redirect('student_log_in')

    marks = MarksDb.objects.filter(student=student_name)

    return render(request, 'Student_Internal_Marks.html', {
        'marks': marks
    })


def student_notifications(request):
    return render(request, 'Student_notifications.html')
#
# def student_support(request):
#     return render(request, 'student/support.html')
#

def student_dashboard(request):
    student_name = request.session.get('student_name')

    if not student_name:
        return redirect('student_log_in')

    return render(request, 'student_index.html', {
        'student_name': student_name
    })

def student_semester_results(request):
    student_name = request.session.get('student_name')

    if not student_name:
        return redirect('student_log_in')

    student = StudentDb.objects.get(name=student_name)

    results = MarksDb.objects.filter(
        student=student.name,
        semester=student.semester
    )

    return render(request, 'Student_Semester_Results.html', {
        'results': results
    })

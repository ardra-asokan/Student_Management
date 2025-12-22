from django.shortcuts import render,redirect, get_object_or_404
from Adminapp.models import SubjectDb,StudentDb,AssignedSubjectDb,AnnouncementDb
from teacherapp.models import AttendanceDb,MarksDb,AssignmentSubmissionDb,AssignmentDb,StudyMaterialDb
from django.db.models import Count, Q
from django.utils import timezone
from django.db.models import Avg, Sum, Count
from django.contrib import messages
from .models import LeaveApplicationDb


# Create your views here.
def student_page(request):
    student_id = request.session.get('student_id')

    if not student_id:
        return redirect('student_log_in')

    student = StudentDb.objects.get(id=student_id)

    # Subject count
    subject_count = SubjectDb.objects.filter(
        department=student.department,
        semester=student.semester
    ).count()

    # Pending assignments
    pending_assignments = AssignmentDb.objects.filter(
        subject__department=student.department,
        subject__semester=student.semester
    ).count()

    # Announcements
    announcement_count = AnnouncementDb.objects.filter(
        sender_type__in=["Admin", "Teacher"]
    ).count()

    return render(request, "Student_index.html", {
        "subject_count": subject_count,
        "pending_assignments": pending_assignments,
        "announcement_count": announcement_count
    })

def student_profile(request):
    student_id = request.session.get("student_id")

    if not student_id:
        return redirect("student_login")

    try:
        student = StudentDb.objects.get(id=student_id)
    except StudentDb.DoesNotExist:
        # If student record is deleted or invalid session
        return redirect("student_login")

    return render(
        request,
        "View_Student_Profile.html",
        {"student": student}
    )

def student_edit_profile(request):
    student_id = request.session.get('student_id')

    if not student_id:
        return redirect('student_log_in')

    try:
        student = StudentDb.objects.get(id=student_id)
    except StudentDb.DoesNotExist:
        return redirect('student_log_in')

    if request.method == "POST":
        student.email = request.POST.get('email')
        student.phone = request.POST.get('phone')
        student.address = request.POST.get('address')


        if 'photo' in request.FILES:
            student.profile_photo = request.FILES['photo']

        student.save()
        return redirect('studentapp:student_profile')

    return render(request, 'Edit_Student_Profile.html', {
        'student': student
    })

def view_student_subjects(request):
    student_id = request.session.get("student_id")

    if not student_id:
        return redirect("student_log_in")

    student = StudentDb.objects.get(id=student_id)

    subjects = SubjectDb.objects.filter(
        department__iexact=student.department.strip(),
        semester__iexact=student.semester.strip()
    )

    return render(request, "View_Student_Subjects.html", {
        "subjects": subjects,
        "student": student
    })



def student_subject_details(request, subject_id):
    student_id = request.session.get('student_id')

    if not student_id:
        return redirect('student_log_in')

    try:
        student = StudentDb.objects.get(id=student_id)
    except StudentDb.DoesNotExist:
        return redirect('student_log_in')

    subject = SubjectDb.objects.filter(
        id=subject_id,
        department__iexact=student.department,
        semester__iexact=student.semester
    ).first()

    if not subject:
        return redirect('studentapp:view_student_subjects')  # or show error page

    return render(request, 'Student_Subject_Details.html', {
        'subject': subject
    })


def student_attendance(request):
    student_id = request.session.get('student_id')

    if not student_id:
        return redirect('student_log_in')

    attendance_data = (
        AttendanceDb.objects
        .filter(student_id=student_id)
        .values('subject__subject_name')
        .annotate(
            total_classes=Count('id'),
            present_count=Count('id', filter=Q(status__iexact='Present'))
        )
    )

    # calculate percentage
    for a in attendance_data:
        if a['total_classes'] > 0:
            a['percentage'] = round(
                (a['present_count'] / a['total_classes']) * 100, 2
            )
        else:
            a['percentage'] = 0

    return render(request, 'Student_attendance.html', {
        'attendance_data': attendance_data
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
    student_id = request.session.get('student_id')

    if not student_id:
        return redirect('student_log_in')

    marks = MarksDb.objects.filter(student_id=student_id)

    print("MARKS:", marks)  # DEBUG – check terminal

    return render(request, 'student_internal_marks.html', {
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

def pending_assignments(request):
    student_name = request.session.get('student_name')

    if not student_name:
        return redirect('student_log_in')

    # get logged-in student
    student = StudentDb.objects.get(name=student_name)

    # assignments already submitted by this student
    submitted_ids = AssignmentSubmissionDb.objects.filter(
        student=student
    ).values_list('assignment_id', flat=True)

    # pending assignments (not submitted)
    pending_assignments = AssignmentDb.objects.exclude(
        id__in=submitted_ids
    )

    return render(request, 'Pending_Assignments.html', {
        'assignments': pending_assignments
    })



def student_upload_assignment(request):
    student_name = request.session.get('student_name')

    if not student_name:
        return redirect('student_log_in')

    student = StudentDb.objects.get(name=student_name)

    # assignments not yet submitted by this student
    submitted_ids = AssignmentSubmissionDb.objects.filter(
        student=student
    ).values_list('assignment_id', flat=True)

    assignments = AssignmentDb.objects.exclude(id__in=submitted_ids)

    if request.method == "POST":
        assignment_id = request.POST.get('assignment')
        file = request.FILES.get('file')

        assignment = AssignmentDb.objects.get(id=assignment_id)

        AssignmentSubmissionDb.objects.create(
            assignment=assignment,
            student=student,
            file=file,
            submitted_at=timezone.now()
        )

        return redirect('studentapp:submitted_assignments')

    return render(request, 'Student_Upload_Assignments.html', {
        'assignments': assignments
    })

def submitted_assignments(request):
    student_name = request.session.get('student_name')

    if not student_name:
        return redirect('student_log_in')

    student = StudentDb.objects.get(name=student_name)

    submissions = AssignmentSubmissionDb.objects.filter(
        student=student
    ).select_related('assignment', 'assignment__subject')

    return render(request, 'Submitted_Assignments.html', {
        'submissions': submissions
    })

def student_announcements(request):
    student_id = request.session.get('student_id')

    if not student_id:
        return redirect('student_log_in')

    announcements = AnnouncementDb.objects.all().order_by('-created_at')

    return render(request, 'Student_Announcements.html', {
        'announcements': announcements
    })


def student_study_materials(request):
    student_name = request.session.get('student_name')

    if not student_name:
        return redirect('student_log_in')

    materials = StudyMaterialDb.objects.select_related(
        'subject', 'teacher'
    ).order_by('-uploaded_at')

    return render(request, 'Student_Study_Materials.html', {
        'materials': materials
    })

def student_download_marksheet(request):
    student_id = request.session.get("student_id")

    if not student_id:
        return redirect("student_log_in")

    return render(request, "Student_download_marksheets.html")
def student_leave_application(request):
    student_name = request.session.get("student_name")

    if not student_name:
        return redirect("student_login")

    if request.method == "POST":
        subject = request.POST.get("subject")
        from_date = request.POST.get("from_date")
        to_date = request.POST.get("to_date")
        reason = request.POST.get("reason")

        LeaveApplicationDb.objects.create(
            student_name=student_name,
            subject=subject,
            from_date=from_date,
            to_date=to_date,
            reason=reason
        )

        messages.success(request, "Leave application submitted successfully")
        return redirect("studentapp:leave_application")

    return render(request, "Student_leave_application.html")

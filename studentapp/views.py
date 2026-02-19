from django.shortcuts import render,redirect, get_object_or_404
from Adminapp.models import SubjectDb,StudentDb,AssignedSubjectDb,AnnouncementDb
from teacherapp.models import AttendanceDb,MarksDb,AssignmentSubmissionDb,AssignmentDb,StudyMaterialDb
from django.db.models import Count, Q
from django.utils import timezone
from django.db.models import Avg, Sum, Count
from django.contrib import messages
from studentapp.models import LeaveApplicationDb
from django.utils.timesince import timesince
from chat.models import ChatMessageDb


# Create your views here.
def student_page(request):
    student_name = request.session.get('student_name')

    if not student_name:
        messages.error(request, "Please login to access the dashboard")
        return redirect('student_log_in')

    messages.success(request, f"Welcome {student_name}")

    return render(request, 'Student_index.html', {
        'student_name': student_name
    })


def student_profile(request):
    student_id = request.session.get("student_id")

    if not student_id:
        messages.error(request, "Please login to view your profile")
        return redirect("student_login")

    try:
        student = StudentDb.objects.get(id=student_id)
    except StudentDb.DoesNotExist:
        messages.error(request, "Your profile is not available. Please login again")
        return redirect("student_login")

    messages.success(request, "Profile loaded successfully")

    return render(request,"View_Student_Profile.html",
        {"student": student}
    )

def student_edit_profile(request):
    student_id = request.session.get('student_id')

    if not student_id:
        messages.error(request, "Please login to edit your profile")
        return redirect('student_log_in')

    try:
        student = StudentDb.objects.get(id=student_id)
    except StudentDb.DoesNotExist:
        messages.error(request, "Invalid session. Please login again")
        return redirect('student_log_in')

    if request.method == "POST":
        student.email = request.POST.get('email')
        student.phone = request.POST.get('phone')
        student.address = request.POST.get('address')

        if 'photo' in request.FILES:
            student.profile_photo = request.FILES['photo']

        student.save()
        messages.success(request, "Profile updated successfully")
        return redirect('studentapp:student_profile')

    messages.info(request, "You can update your profile details here")

    return render(request, 'Edit_Student_Profile.html', {
        'student': student
    })

def view_student_subjects(request):
    student_id = request.session.get("student_id")

    if not student_id:
        messages.error(request, "Please login to view subjects")
        return redirect("student_log_in")

    try:
        student = StudentDb.objects.get(id=student_id)
    except StudentDb.DoesNotExist:
        messages.error(request, "Invalid session. Please login again")
        return redirect("student_log_in")

    subjects = SubjectDb.objects.filter(
        department__iexact=student.department.strip(),
        semester__iexact=student.semester.strip()
    )

    if not subjects.exists():
        messages.info(request, "No subjects found for your department and semester")
    else:
        messages.success(request, "Subjects loaded successfully")

    return render(request, "View_Student_Subjects.html", {
        "subjects": subjects,
        "student": student
    })


def student_subject_details(request, subject_id):
    student_id = request.session.get('student_id')

    if not student_id:
        messages.error(request, "Please login to view subject details")
        return redirect('student_log_in')

    try:
        student = StudentDb.objects.get(id=student_id)
    except StudentDb.DoesNotExist:
        messages.error(request, "Invalid session. Please login again")
        return redirect('student_log_in')

    subject = SubjectDb.objects.filter(
        id=subject_id,
        department__iexact=student.department,
        semester__iexact=student.semester
    ).first()

    if not subject:
        messages.error(request, "You are not authorized to view this subject")
        return redirect('studentapp:view_student_subjects')

    messages.success(request, "Subject details loaded successfully")

    return render(request, 'Student_Subject_Details.html', {
        'subject': subject
    })


def student_attendance(request):
    student_id = request.session.get('student_id')

    if not student_id:
        messages.error(request, "Please login to view attendance")
        return redirect('student_log_in')

    attendance_data = (AttendanceDb.objects.filter(student_id=student_id)
        .values('subject__subject_name')
        .annotate(total_classes=Count('id'),present_count=Count('id', filter=Q(status__iexact='Present'))
        )
    )

    for a in attendance_data:
        if a['total_classes'] > 0:
            a['percentage'] = round(
                (a['present_count'] / a['total_classes']) * 100, 2
            )
        else:
            a['percentage'] = 0

    if not attendance_data:
        messages.info(request, "Attendance not available yet")
    else:
        messages.success(request, "Attendance details loaded")

    return render(request, 'Student_attendance.html', {
        'attendance_data': attendance_data
    })

def student_timetable(request):
    return render(request, 'Student_timetable.html')

def student_assignments(request):
    student_name = request.session.get('student_name')

    if not student_name:
        messages.error(request, "Please login to view assignments")
        return redirect('student_log_in')

    try:
        student = StudentDb.objects.get(name=student_name)
    except StudentDb.DoesNotExist:
        messages.error(request, "Invalid session. Please login again")
        return redirect('student_log_in')

    assignments = AssignmentDb.objects.filter(
        class_name=student.class_name,
        semester=student.semester
    )

    if not assignments.exists():
        messages.info(request, "No assignments available right now")
    else:
        messages.success(request, "Assignments loaded successfully")

    return render(request, 'Student_Assignments.html', {
        'assignments': assignments
    })

def student_internal_marks(request):
    student_id = request.session.get('student_id')

    if not student_id:
        messages.error(request, "Please login to view internal marks")
        return redirect('student_log_in')

    marks = MarksDb.objects.filter(student_id=student_id)

    if not marks.exists():
        messages.info(request, "Internal marks are not available yet")
    else:
        messages.success(request, "Internal marks loaded successfully")


    return render(request, 'Student_Internal_Marks.html', {
        'marks': marks
    })


def student_notifications(request):
    return render(request, 'Student_notifications.html')


def student_dashboard(request):
    student_id = request.session.get('student_id')

    if not student_id:
        messages.error(request, "Please login to continue")
        return redirect('student_log_in')

    student = StudentDb.objects.get(id=student_id)

    # ---------------- SUBJECT COUNT ----------------
    subject_count = SubjectDb.objects.filter(
        department=student.department,
        semester=student.semester
    ).count()

    # ---------------- PENDING ASSIGNMENTS ----------------
    all_assignments = AssignmentDb.objects.filter(
        subject__department=student.department,
        subject__semester=student.semester
    )

    submitted_ids = AssignmentSubmissionDb.objects.filter(
        student=student
    ).values_list('assignment_id', flat=True)

    pending_assignments = all_assignments.exclude(
        id__in=submitted_ids
    ).count()

    # ---------------- ATTENDANCE % ----------------
    attendance_qs = AttendanceDb.objects.filter(student=student)
    total_classes = attendance_qs.count()
    present_classes = attendance_qs.filter(status__iexact="Present").count()

    attendance_percent = round(
        (present_classes / total_classes) * 100, 2
    ) if total_classes > 0 else 0

    # ---------------- ANNOUNCEMENTS ----------------
    announcements = AnnouncementDb.objects.filter(
        sender_type__in=["Admin", "Teacher"]
    ).order_by("-created_at")[:5]

    # ----------------  TEACHER → STUDENT CHAT MESSAGES ----------------
    student_messages = ChatMessageDb.objects.filter(
        sender_teacher__isnull=False,   # message sent by teacher
        sender_student=student          # message for this student
    ).order_by("-timestamp")[:5]

    message_count = student_messages.count()

    return render(request, "Student_index.html", {
        # Dashboard cards
        "subject_count": subject_count,
        "pending_assignments": pending_assignments,
        "attendance_percent": attendance_percent,

        # Announcements
        "announcement_count": announcements.count(),
        "announcements": announcements,

        # Messages
        "student_messages": student_messages,
        "message_count": message_count,
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
        messages.error(request, "Please login to view pending assignments")
        return redirect('student_log_in')

    try:
        student = StudentDb.objects.get(name=student_name)
    except StudentDb.DoesNotExist:
        messages.error(request, "Invalid session. Please login again")
        return redirect('student_log_in')


    submitted_ids = AssignmentSubmissionDb.objects.filter(
        student=student
    ).values_list('assignment_id', flat=True)

    pending_assignments = AssignmentDb.objects.exclude(
        id__in=submitted_ids
    )

    if not pending_assignments.exists():
        messages.info(request, "No pending assignments")
    else:
        messages.success(request, "Pending assignments loaded")

    return render(request, 'Pending_Assignments.html', {
        'assignments': pending_assignments
    })


def student_upload_assignment(request):
    student_name = request.session.get('student_name')

    if not student_name:
        messages.error(request, "Please login to upload assignments")
        return redirect('student_log_in')

    try:
        student = StudentDb.objects.get(name=student_name)
    except StudentDb.DoesNotExist:
        messages.error(request, "Invalid session. Please login again")
        return redirect('student_log_in')

    # assignments not yet submitted by this student
    submitted_ids = AssignmentSubmissionDb.objects.filter(
        student=student
    ).values_list('assignment_id', flat=True)

    assignments = AssignmentDb.objects.exclude(id__in=submitted_ids)

    if request.method == "POST":
        assignment_id = request.POST.get('assignment')
        file = request.FILES.get('file')

        if not assignment_id or not file:
            messages.error(request, "Please select an assignment and upload a file")
            return redirect('studentapp:student_upload_assignment')

        assignment = AssignmentDb.objects.get(id=assignment_id)

        AssignmentSubmissionDb.objects.create(
            assignment=assignment,
            student=student,
            file=file,
            submitted_at=timezone.now()
        )

        messages.success(request, "Assignment uploaded successfully")
        return redirect('studentapp:submitted_assignments')

    messages.info(request, "Upload your pending assignments here")

    return render(request, 'Student_Upload_Assignments.html', {
        'assignments': assignments
    })


def submitted_assignments(request):
    student_name = request.session.get('student_name')

    if not student_name:
        messages.error(request, "Please login to view submitted assignments")
        return redirect('student_log_in')

    try:
        student = StudentDb.objects.get(name=student_name)
    except StudentDb.DoesNotExist:
        messages.error(request, "Invalid session. Please login again")
        return redirect('student_log_in')

    submissions = AssignmentSubmissionDb.objects.filter(
        student=student
    ).select_related('assignment', 'assignment__subject')

    if not submissions.exists():
        messages.info(request, "You have not submitted any assignments yet")
    else:
        messages.success(request, "Submitted assignments loaded successfully")

    return render(request, 'Submitted_Assignments.html', {
        'submissions': submissions
    })


def student_announcements(request):
    student_id = request.session.get('student_id')

    if not student_id:
        messages.error(request, "Please login to view announcements")
        return redirect('student_log_in')

    student = StudentDb.objects.get(id=student_id)

    # Get teachers assigned to this student's department & semester
    assigned_subjects = AssignedSubjectDb.objects.filter(
        class_name__icontains=student.department,
        semester=student.semester
    )

    teacher_names = assigned_subjects.values_list('teacher', flat=True)

    # Filter announcements
    announcements = AnnouncementDb.objects.filter(
        Q(sender_type="Admin") |
        Q(sender_type="Teacher", sender_name__in=teacher_names)
    ).order_by('-created_at')

    if not announcements.exists():
        messages.info(request, "No announcements available for your class")
    else:
        messages.success(request, "Latest announcements loaded")

    return render(request, 'Student_Announcements.html', {
        'announcements': announcements
    })


def student_study_materials(request):
    student_id = request.session.get('student_id')

    if not student_id:
        messages.error(request, "Please login to view study materials")
        return redirect('student_log_in')

    student = StudentDb.objects.get(id=student_id)

    # Filter materials based on student's department and semester
    materials = StudyMaterialDb.objects.select_related(
        'subject', 'teacher'
    ).filter(
        subject__department=student.department,
        subject__semester=student.semester
    ).order_by('-uploaded_at')

    if not materials.exists():
        messages.info(request, "No study materials available for your class yet")
    else:
        messages.success(request, "Study materials loaded successfully")

    return render(request, 'Student_Study_Materials.html', {
        'materials': materials
    })



def student_download_marksheet(request):
    student_id = request.session.get("student_id")

    if not student_id:
        messages.error(request, "Please login to download marksheets")
        return redirect("student_log_in")

    messages.info(request, "You can download your marksheets from here")

    return render(request, "Student_download_marksheets.html")

def student_leave_application(request):
    student_name = request.session.get("student_name")

    if not student_name:
        messages.error(request, "Please login to apply for leave")
        return redirect("student_login")

    if request.method == "POST":
        subject = request.POST.get("subject")
        from_date = request.POST.get("from_date")
        to_date = request.POST.get("to_date")
        reason = request.POST.get("reason")

        if not subject or not from_date or not to_date or not reason:
            messages.error(request, "All fields are required")
            return redirect("studentapp:leave_application")

        LeaveApplicationDb.objects.create(
            student_name=student_name,
            subject=subject,
            from_date=from_date,
            to_date=to_date,
            reason=reason
        )

        messages.success(request, "Leave application submitted successfully")
        return redirect("studentapp:leave_application")

    messages.info(request, "Fill the form to apply for leave")

    return render(request, "Student_leave_application.html")

from django.shortcuts import render,redirect
from Adminapp.models import SubjectDb,AssignedSubjectDb,StudentDb,TeacherDb,AnnouncementDb
from teacherapp.models import AttendanceDb,MarksDb,AssignmentDb,AssignmentSubmissionDb,StudyMaterialDb
from datetime import date,datetime
from django.contrib import messages
import os
from django.conf import settings
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from chat.models import ChatMessageDb
from django.utils import timezone


# Create your views here.
def teacher_page(request):
    messages.success(request, "Welcome to Teacher Dashboard")
    return render(request, "teacher_index.html")

def teacher_assigned_subjects(request):
    teacher_id = request.session.get("teacher_id")

    if not teacher_id:
        messages.error(request, "Please login to view your assigned subjects")
        return redirect("teacher_log_in")

    data = AssignedSubjectDb.objects.filter(teacher_id=teacher_id)

    if not data.exists():
        messages.info(request, "No subjects assigned to you yet")
    else:
        messages.success(request, "Assigned subjects loaded successfully")

    return render(request, 'teacher_assigned_subjects.html', {'data': data})

def view_subjects(request):
    teacher_name = request.session.get('teacher_name')

    if not teacher_name:
        messages.error(request, "Please login to view subjects")
        return redirect('teacher_log_in')

    data = AssignedSubjectDb.objects.filter(
        teacher=teacher_name
    ).select_related('subject')

    if not data.exists():
        messages.info(request, "No subjects assigned yet")
    else:
        messages.success(request, "Subjects loaded successfully")

    return render(request, "View_subjects.html", {"data": data})

def teacher_dashboard(request):
    teacher_name = request.session.get("teacher_name")

    if not teacher_name:
        messages.error(request, "Please login to access the dashboard")
        return redirect("teacher_log_in")

    # ---------------- SUBJECTS ----------------
    assigned_subjects = AssignedSubjectDb.objects.filter(
        teacher=teacher_name
    ).select_related("subject")

    subject_count = assigned_subjects.count()

    # ---------------- STUDENTS ----------------
    departments = assigned_subjects.values_list(
        "subject__department", flat=True
    )
    semesters = assigned_subjects.values_list(
        "subject__semester", flat=True
    )

    student_count = StudentDb.objects.filter(
        department__in=departments,
        semester__in=semesters
    ).count()

    # ---------------- ATTENDANCE ----------------
    subjects = assigned_subjects.values_list("subject", flat=True)

    attendance_done = AttendanceDb.objects.filter(
        subject__in=subjects
    ).count()

    # ---------------- ASSIGNMENTS ----------------
    assignment_count = AssignmentDb.objects.filter(
        subject__in=subjects
    ).count()

    # ---------------- ADMIN → TEACHER NOTIFICATIONS ----------------
    admin_notifications = AnnouncementDb.objects.filter(
        sender_type="Admin"
    ).order_by("-created_at")[:5]

    notification_count = admin_notifications.count()

    # ---------------- STUDENT → TEACHER CHAT MESSAGES ----------------
    teacher = TeacherDb.objects.get(name=teacher_name)

    student_messages = ChatMessageDb.objects.filter(
        sender_student__isnull=False,
        sender_teacher__isnull=True
    ).order_by("-timestamp")[:5]

    message_count = student_messages.count()

    # ---------------- RENDER ----------------
    return render(request, "teacher_index.html", {
        "teacher_name": teacher_name,

        # Dashboard cards
        "subject_count": subject_count,
        "student_count": student_count,
        "attendance_done": attendance_done,
        "assignment_count": assignment_count,

        # Notifications
        "admin_notifications": admin_notifications,
        "notification_count": notification_count,

        # Messages
        "student_messages": student_messages,
        "message_count": message_count,
    })




def mark_attendance(request):
    teacher_name = request.session.get('teacher_name')

    if not teacher_name:
        messages.error(request, "Please login to mark attendance")
        return redirect('teacher_log_in')

    assigned_subjects = AssignedSubjectDb.objects.filter(
        teacher=teacher_name
    )

    selected_subject = request.GET.get('subject')
    department = request.GET.get('department')
    semester = request.GET.get('semester')

    students = StudentDb.objects.none()

    if selected_subject and department and semester:
        students = StudentDb.objects.filter(
            department=department,
            semester=semester
        )

        if not students.exists():
            messages.info(request, "No students found for the selected class")
        else:
            messages.success(request, "Student list loaded for attendance")

    else:
        messages.info(request, "Please select subject, department, and semester")

    return render(request, "Mark_attendance.html", {
        "assigned_subjects": assigned_subjects,
        "students": students,
        "selected_subject": selected_subject,
        "department": department,
        "semester": semester,
        "today": date.today(),
    })

def save_attendance(request):
    if request.method == "POST":

        assigned_subject_id = request.POST.get("subject_id")

        if not assigned_subject_id:
            messages.error(request, "Subject not selected")
            return redirect("teacherapp:mark_attendance")

        assigned_subject = AssignedSubjectDb.objects.get(id=assigned_subject_id)
        subject = assigned_subject.subject

        att_date_str = request.POST.get("att_date")

        if att_date_str:
            try:
                att_date = datetime.strptime(att_date_str, "%Y-%m-%d").date()
            except ValueError:
                att_date = datetime.strptime(att_date_str, "%b. %d, %Y").date()
        else:
            att_date = date.today()

        attendance_marked = False

        for key, value in request.POST.items():
            if key.startswith("student_"):
                student_id = key.split("_")[1]
                student = StudentDb.objects.get(id=student_id)

                AttendanceDb.objects.update_or_create(
                    student=student,
                    subject=subject,
                    date=att_date,
                    defaults={"status": value}
                )
                attendance_marked = True

        if attendance_marked:
            messages.success(request, "Attendance saved successfully")
        else:
            messages.warning(request, "No attendance data was submitted")

        return redirect("teacherapp:teacher_view_attendance")

def teacher_view_attendance(request):
    teacher_name = request.session.get("teacher_name")

    if not teacher_name:
        messages.error(request, "Please login to view attendance")
        return redirect("teacher_log_in")

    assigned_subjects = AssignedSubjectDb.objects.filter(
        teacher=teacher_name
    ).select_related("subject")

    selected_date = request.GET.get("date")
    selected_subject_id = request.GET.get("subject")

    records = None

    if selected_date and selected_subject_id:
        try:
            selected_date = datetime.strptime(selected_date, "%Y-%m-%d").date()
        except ValueError:
            messages.error(request, "Invalid date format")
            selected_date = None

        if selected_date:
            records = AttendanceDb.objects.filter(
                date=selected_date,
                subject_id=selected_subject_id
            ).select_related("student", "subject")

            if not records.exists():
                messages.info(request, "No attendance records found for the selected date and subject")
            else:
                messages.success(request, "Attendance records loaded successfully")
    else:
        messages.info(request, "Please select subject and date to view attendance")

    return render(request, "Teacher_view_attendance.html", {
        "assigned_subjects": assigned_subjects,
        "records": records,
        "selected_date": selected_date,
        "selected_subject": selected_subject_id,
    })

def upload_marks(request):
    teacher_name = request.session.get('teacher_name')

    if not teacher_name:
        messages.error(request, "Please login to upload marks")
        return redirect('teacher_log_in')

    assigned_subjects = AssignedSubjectDb.objects.filter(
        teacher__iexact=teacher_name.strip()
    ).select_related('subject')

    students = []
    selected_assigned_id = request.GET.get("subject")
    selected_exam = request.GET.get("exam")

    if selected_assigned_id and selected_exam:
        assigned = AssignedSubjectDb.objects.filter(
            id=selected_assigned_id,
            teacher__iexact=teacher_name.strip()
        ).select_related('subject').first()

        if assigned and assigned.subject:
            department = assigned.subject.department
            semester = assigned.subject.semester

            students = StudentDb.objects.filter(
                department__iexact=department.strip(),
                semester__iexact=semester.strip()
            )

            if not students.exists():
                messages.info(request, "No students found for the selected subject")
            else:
                messages.success(request, "Student list loaded for mark entry")
        else:
            messages.info(request, "Please select subject and exam type")


    return render(request, "Upload_marks.html", {
        "assigned_subjects": assigned_subjects,
        "students": students,
        "selected_subject": selected_assigned_id,
        "selected_exam": selected_exam,
    })


def save_marks(request):
    if request.method == "POST":

        exam_type = request.POST.get("exam_type")
        assigned_id = request.POST.get("assigned_id")

        if not exam_type or not assigned_id:
            messages.error(request, "Exam type or subject not selected")
            return redirect("teacherapp:upload_marks")


        assigned = AssignedSubjectDb.objects.get(id=assigned_id)
        subject = assigned.subject

        marks_saved = False


        for key, value in request.POST.items():
            if key.startswith("marks_"):
                student_id = key.split("_")[1]
                marks = value

                if marks == "":
                    continue


                MarksDb.objects.create(
                    student_id=student_id,
                    subject=subject,
                    exam_type=exam_type,
                    marks=marks,
                    date=date.today()
                )
                marks_saved = True

        if marks_saved:
            messages.success(request, "Marks saved successfully ")
        else:
            messages.warning(request, "No marks were entered")

        return redirect("teacherapp:upload_marks")

def teacher_view_marks(request):
    teacher_name = request.session.get("teacher_name")

    if not teacher_name:
        messages.error(request, "Please login to view marks")
        return redirect("teacher_log_in")

    assigned_subjects = AssignedSubjectDb.objects.filter(teacher=teacher_name).select_related('subject')

    marks = None
    selected_subject = request.GET.get("subject")
    selected_exam = request.GET.get("exam")

    if selected_subject and selected_exam:
        marks = MarksDb.objects.filter(subject_id=selected_subject,exam_type=selected_exam).select_related('student')

        if not marks.exists():
            messages.info(request, "No marks found for the selected subject and exam")
        else:
            messages.success(request, "Marks loaded successfully")
    else:
        messages.info(request, "Please select subject and exam to view marks")

    return render(request, "Teacher_view_marks.html", {
        "assigned_subjects": assigned_subjects,
        "marks": marks,
        "selected_subject": selected_subject,
        "selected_exam": selected_exam,
    })

def edit_marks(request, mark_id):
    mark = MarksDb.objects.select_related("student", "subject").get(id=mark_id)

    return render(request, "Teacher_Edit_Marks.html", {
        "mark": mark
    })

def update_marks(request, mark_id):
    if request.method == "POST":
        new_marks = request.POST.get("marks")

        if new_marks == "" or new_marks is None:
            messages.error(request, "Marks cannot be empty")
            return redirect("teacherapp:edit_marks", mark_id=mark_id)

        updated = MarksDb.objects.filter(id=mark_id).update(
            marks=new_marks,
            date=date.today()
        )

        if updated:
            messages.success(request, "Marks updated successfully")
        else:
            messages.error(request, "Failed to update marks")

        return redirect("teacherapp:teacher_view_marks")


def delete_mark(request, mark_id):
    mark = MarksDb.objects.get(id=mark_id)
    mark.delete()
    messages.success(request, "Mark deleted successfully")
    return redirect('teacherapp:teacher_view_marks')


def upload_assignments(request):
    teacher_id = request.session.get("teacher_id")
    teacher_name = request.session.get("teacher_name")

    if not teacher_id or not teacher_name:
        messages.error(request, "Please login to manage assignments")
        return redirect("teacher_log_in")

    assigned_subjects = AssignedSubjectDb.objects.filter(
        teacher=teacher_name
    ).select_related("subject")


    assignments = AssignmentDb.objects.filter(
        teacher_id=teacher_id
    ).order_by("-id")


    return render(request, "Upload_Assignments.html", {
        "assigned_subjects": assigned_subjects,
        "assignments": assignments,
    })



def save_assignment(request):
    if request.method == "POST":
        subject_id = request.POST.get("subject")
        title = request.POST.get("title")
        deadline = request.POST.get("deadline")
        file = request.FILES.get("assignment_file")
        teacher_id = request.session.get("teacher_id")


        subject = SubjectDb.objects.get(id=subject_id)

        AssignmentDb.objects.create(teacher_id=teacher_id,subject=subject,title=title, deadline=deadline, assignment_file=file)

        messages.success(request, "Assignment uploaded successfully!")
        return redirect("teacherapp:upload_assignments")


def student_submissions(request):
    teacher_id = request.session.get("teacher_id")

    if not teacher_id:
        messages.error(request, "Please login to view student submissions")
        return redirect("teacher_log_in")

    assignments = AssignmentDb.objects.filter(teacher_id=teacher_id)

    selected_assignment = request.GET.get("assignment_id")

    submissions = []

    if selected_assignment:
        submissions = AssignmentSubmissionDb.objects.filter(
            assignment_id=selected_assignment
        ).select_related("student")


    return render(request, "Student_submissions.html", {
        "assignments": assignments,
        "selected_assignment": selected_assignment,
        "submissions": submissions,
    })


def grade_assignments(request):
    teacher_id = request.session.get("teacher_id")

    assignments = AssignmentDb.objects.filter(teacher_id=teacher_id)
    selected_assignment = request.GET.get("assignment_id")

    submissions = []
    if selected_assignment:
        submissions = AssignmentSubmissionDb.objects.filter(
            assignment_id=selected_assignment
        ).select_related("student")

    return render(request, "grade_assignments.html", {
        "assignments": assignments,
        "selected_assignment": selected_assignment,
        "submissions": submissions,
    })

def save_assignment_grades(request):
    if request.method == "POST":
        assignment_id = request.POST.get("assignment_id")

        submissions = AssignmentSubmissionDb.objects.filter(assignment_id=assignment_id)

        for sb in submissions:
            marks = request.POST.get(f"marks_{sb.id}")
            sb.marks = marks
            sb.save()

        messages.success(request, "Grades saved successfully!")
        return redirect("teacherapp:grade_assignments")


def view_students(request):
    teacher_name = request.session.get('teacher_name')

    assigned_subjects = AssignedSubjectDb.objects.filter(teacher=teacher_name)

    students = StudentDb.objects.none()

    if assigned_subjects.exists():
        departments = []

        for a in assigned_subjects:
            if a.class_name:
                departments.append(a.class_name.split()[0].strip())

        students = StudentDb.objects.filter(
            department__in=departments
        )

    return render(request, "View_Students.html", {
        "students": students
    })


def search_students(request):
    students = StudentDb.objects.all()

    name = request.GET.get("name")
    roll = request.GET.get("roll")
    department = request.GET.get("department")
    semester = request.GET.get("semester")

    if name:
        students = students.filter(name__icontains=name)

    if roll:
        students = students.filter(roll_no__icontains=roll)

    if department:
        students = students.filter(department__iexact=department)

    if semester:
        students = students.filter(semester__iexact=semester)

    return render(request, "Search_Students.html", {
        "students": students,
    })



def teacher_student_profile(request,student_id):
    student = StudentDb.objects.get(id=student_id)

    total = AttendanceDb.objects.filter(student=student).count()
    present = AttendanceDb.objects.filter(student=student, status="Present").count()
    percent = round((present / total * 100), 2) if total > 0 else 0

    submissions = AssignmentSubmissionDb.objects.filter(student=student)
    submitted = submissions.count()
    average = submissions.aggregate(avg=Avg('marks'))['avg'] or 0

    return render(request, "Student_Profile.html", {
        "student": student,
        "attendance": {
            "total": total,
            "present": present,
            "percent": percent
        },
        "assignment": {
            "submitted": submitted,
            "average": round(average, 2)
        }
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

    return render(request, 'student_semester_results.html', {
        'results': results
    })


def delete_assignment(request, assignment_id):
    teacher_id = request.session.get("teacher_id")

    if not teacher_id:
        return redirect("teacher_log_in")

    assignment = get_object_or_404(AssignmentDb,id=assignment_id,teacher_id=teacher_id)

    if assignment.assignment_file:
        file_path = assignment.assignment_file.path
        if os.path.exists(file_path):
            os.remove(file_path)

    assignment.delete()
    messages.success(request, "Assignment deleted successfully")
    return redirect("teacherapp:upload_assignments")

def teacher_send_announcements(request):
    teacher_name = request.session.get("teacher_name")

    if request.method == "POST":
        title = request.POST.get("title")
        message = request.POST.get("message")

        AnnouncementDb.objects.create(
            title=title,
            message=message,
            sender_type="Teacher",
            sender_name=teacher_name
        )
        messages.success(request, "Announcement sent successfully")
        return redirect("teacherapp:teacher_view_announcements")

    return render(request, "Teacher_Send_Announcements.html")

def teacher_view_announcements(request):
    announcements = AnnouncementDb.objects.all().order_by('-created_at')

    if not announcements.exists():
        messages.info(request, "No announcements available")
    else:
        messages.success(request, "Announcements loaded successfully")

    return render(request, "Teacher_View_Announcements.html", {
        "announcements": announcements
    })

def upload_study_material(request):
    teacher_id = request.session.get("teacher_id")
    teacher = TeacherDb.objects.get(id=teacher_id)

    assigned_subjects = AssignedSubjectDb.objects.filter(teacher=teacher)

    if request.method == "POST":
        subject_id = request.POST.get("subject")
        title = request.POST.get("title")
        description = request.POST.get("description")
        file = request.FILES.get("material_file")

        subject = SubjectDb.objects.get(id=subject_id)

        StudyMaterialDb.objects.create(teacher=teacher,subject=subject,title=title,description=description,material_file=file)
        messages.success(request, "Study material uploaded successfully")
        return redirect("teacherapp:upload_study_material")

    return render(request, "Upload_Study_materials.html", {
        "assigned_subjects": assigned_subjects
    })

def teacher_view_study_material(request):
    teacher_id = request.session.get("teacher_id")
    teacher = TeacherDb.objects.get(id=teacher_id)

    materials = StudyMaterialDb.objects.filter(teacher=teacher).order_by('-uploaded_at')

    return render(request, "Teacher_View_Study_Material.html", {
        "materials": materials
    })

def delete_study_material(request, material_id):
    material = get_object_or_404(StudyMaterialDb, id=material_id)
    material.delete()
    messages.success(request, "Study material deleted successfully")
    return redirect('teacherapp:teacher_view_study_material')


from django.shortcuts import render,redirect
from Adminapp.models import SubjectDb,AssignedSubjectDb,StudentDb,TeacherDb,AnnouncementDb
from teacherapp.models import AttendanceDb,MarksDb,AssignmentDb,AssignmentSubmissionDb,StudyMaterialDb
from datetime import date
from django.contrib import messages
import os
from django.conf import settings
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.db.models import Avg

from django.utils import timezone


# Create your views here.
def teacher_page(request):
    return render(request, "teacher_index.html")

def teacher_assigned_subjects(request):
    teacher_id = request.session.get("teacher_id")

    if not teacher_id:
        return redirect("teacher_log_in")

    data = AssignedSubjectDb.objects.filter(teacher_id=teacher_id)

    return render(request, 'teacher_assigned_subjects.html', {'data': data})

def view_subjects(request):
    teacher_name = request.session.get('teacher_name')

    if not teacher_name:
        return redirect('teacher_log_in')

    data = AssignedSubjectDb.objects.filter(
        teacher=teacher_name
    ).select_related('subject')

    return render(request, "View_subjects.html", {"data": data})


def search_subjects(request):
    teacher_name = request.session.get('teacher_name')

    qs = AssignedSubjectDb.objects.filter(
        teacher=teacher_name
    )

    return render(request, "Search_Subjects.html", {
        'subjects': qs
    })





def teacher_dashboard(request):
    teacher_name = request.session.get('teacher_name')

    if not teacher_name:
        return redirect('teacher_log_in')

    return render(request, 'teacher_index.html', {
        'teacher_name': teacher_name
    })






def mark_attendance(request):
    teacher_name = request.session.get('teacher_name')

    if not teacher_name:
        return redirect('teacher_log_in')

    assigned_subjects = AssignedSubjectDb.objects.filter(
        teacher=teacher_name
    )

    selected_subject = request.GET.get('subject')
    department = request.GET.get('department')
    semester = request.GET.get('semester')

    students = StudentDb.objects.none()  # ✅ IMPORTANT

    if selected_subject and department and semester:
        students = StudentDb.objects.filter(
            department=department,
            semester=semester
        )

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

        assigned_subject = AssignedSubjectDb.objects.get(
            id=assigned_subject_id
        )

        subject = assigned_subject.subject
        att_date = date.today()

        for key, value in request.POST.items():
            if key.startswith("student_"):
                student_id = key.split("_")[1]

                if not student_id:
                    continue

                student = StudentDb.objects.get(id=student_id)

                AttendanceDb.objects.update_or_create(
                    student=student,
                    subject=subject,
                    date=att_date,
                    defaults={"status": value}
                )

        return redirect("teacherapp:teacher_view_attendance")






def teacher_view_attendance(request):
    teacher_name = request.session.get("teacher_name")

    if not teacher_name:
        return redirect("teacher_log_in")

    selected_date = request.GET.get("date")
    selected_subject = request.GET.get("subject")

    assigned_subjects = AssignedSubjectDb.objects.filter(
        teacher=teacher_name
    ).select_related("subject")  # ✅ This is OK here

    records = None

    if selected_date and selected_subject:
        records = AttendanceDb.objects.filter(
            date=selected_date,
            subject=selected_subject   # ✅ CharField filter
        )

    return render(request, "Teacher_view_attendance.html", {
        "assigned_subjects": assigned_subjects,
        "records": records,
        "selected_date": selected_date,
        "selected_subject": selected_subject,
    })





def teacher_attendance_report(request):
    teacher_name = request.session.get('teacher_name')

    assigned_subjects = AssignedSubjectDb.objects.filter(
        teacher=teacher_name
    )

    selected_subject = request.GET.get("subject")
    selected_date = request.GET.get("date")

    records = AttendanceDb.objects.none()

    if selected_subject and selected_date:
        records = AttendanceDb.objects.filter(
            subject_id=selected_subject,
            date=selected_date
        ).select_related("student", "subject")

    return render(request, "Teacher_Attendance_Report.html", {
        "assigned_subjects": assigned_subjects,
        "records": records,
        "selected_subject": selected_subject,
        "selected_date": selected_date,
    })







def upload_marks(request):
    teacher_name = request.session.get('teacher_name')

    if not teacher_name:
        return redirect('teacher_log_in')

    assigned_subjects = AssignedSubjectDb.objects.filter(
        teacher=teacher_name
    ).select_related('subject')

    return render(request, "Upload_marks.html", {
        "assigned_subjects": assigned_subjects
    })



def teacher_view_marks(request):
    teacher_name = request.session.get("teacher_name")

    assigned_subjects = AssignedSubjectDb.objects.filter(
        teacher=teacher_name
    )

    marks = None
    selected_subject = request.GET.get("subject")

    if selected_subject:
        marks = MarksDb.objects.filter(
            subject_id=selected_subject
        )

    return render(request, "Teacher_view_marks.html", {
        "assigned_subjects": assigned_subjects,
        "marks": marks,
        "selected_subject": selected_subject
    })




def teacher_edit_marks(request, id):
    mark = MarksDb.objects.get(id=id)
    return render(request, "Teacher_Edit_Marks.html", {"mark": mark})

def update_marks(request, id):
    mark = MarksDb.objects.get(id=id)
    if request.method == "POST":
        mark.exam_type = request.POST.get("exam_type")
        mark.marks = request.POST.get("marks")
        mark.save()
        return redirect("teacherapp:view_marks")

def upload_assignments(request):
    teacher_id = request.session.get("teacher_id")
    teacher_name = request.session.get("teacher_name")

    if not teacher_id or not teacher_name:
        return redirect("teacher_log_in")

    # For SUBJECTS → CharField
    assigned_subjects = AssignedSubjectDb.objects.filter(
        teacher=teacher_name
    ).select_related("subject")

    # For ASSIGNMENTS → ForeignKey / ID
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

        AssignmentDb.objects.create(
            teacher_id=teacher_id,
            subject=subject,
            title=title,
            deadline=deadline,
            assignment_file=file
        )


        messages.success(request, "Assignment uploaded successfully!")
        return redirect("teacherapp:upload_assignments")

def student_submissions(request):
    teacher_id = request.session.get("teacher_id")

    # Load assignments created by this teacher
    assignments = AssignmentDb.objects.filter(teacher_id=teacher_id)

    selected_assignment = request.GET.get("assignment_id")

    submissions = []
    if selected_assignment:
        submissions = AssignmentSubmissionDb.objects.filter(
            assignment_id=selected_assignment
        ).select_related("student")

    return render(request, "student_submissions.html", {
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
    teacher_name = request.session.get('Name')

    assigned_subjects = AssignedSubjectDb.objects.filter(
        teacher=teacher_name
    )

    # use assigned_subjects to fetch students
    return render(request, "View_Students.html", {
        'assigned_subjects': assigned_subjects
    })






def search_students(request):
    teacher_id = request.session.get("teacher_id")

    # Classes handled by teacher
    assigned_subjects = AssignedSubjectDb.objects.filter(teacher=teacher_id)
    classes = assigned_subjects.values_list("class_name", flat=True).distinct()

    students = StudentDb.objects.all()

    # Filters
    name = request.GET.get("name")
    roll = request.GET.get("roll")
    class_name = request.GET.get("class_name")
    semester = request.GET.get("semester")

    if name:
        students = students.filter(name__icontains=name)

    if roll:
        students = students.filter(roll_no__icontains=roll)

    if class_name:
        students = students.filter(class_name=class_name)

    if semester:
        students = students.filter(semester=semester)

    return render(request, "Search_Students.html", {
        "students": students,
        "classes": classes,
    })

def student_profile(request):
    student = StudentDb.objects.get(id=student_id)

    # Attendance Summary
    total = AttendanceDb.objects.filter(student=student).count()
    present = AttendanceDb.objects.filter(student=student, status="Present").count()
    percent = round((present / total * 100), 2) if total > 0 else 0

    # Assignment Summary
    submissions = AssignmentSubmissionDb.objects.filter(student=student)
    submitted = submissions.count()
    average = submissions.aggregate(avg=Avg('marks'))['avg'] or 0

    return render(request, "student_profile.html", {
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

    assignment = get_object_or_404(
        AssignmentDb,
        id=assignment_id,
        teacher_id=teacher_id   # ✅ security: only own assignments
    )

    # ✅ delete uploaded file from media folder
    if assignment.assignment_file:
        file_path = assignment.assignment_file.path
        if os.path.exists(file_path):
            os.remove(file_path)

    assignment.delete()


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
        return redirect("teacher_view_announcements")

    return render(request, "Teacher_Send_Announcements.html")

def teacher_view_announcements(request):
    announcements = AnnouncementDb.objects.all().order_by('-created_at')

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

        StudyMaterialDb.objects.create(
            teacher=teacher,
            subject=subject,
            title=title,
            description=description,
            material_file=file
        )

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
    return redirect('teacherapp:teacher_view_study_material')

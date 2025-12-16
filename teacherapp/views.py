from django.shortcuts import render,redirect
from Adminapp.models import SubjectDb,AssignedSubjectDb,StudentDb,TeacherDb
from teacherapp.models import AttendanceDb,MarksDb,AssignmentDb,AssignmentSubmissionDb
from datetime import date
from django.contrib import messages

from django.db.models import Q
from django.shortcuts import get_object_or_404

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

        subject = assigned_subject.subject   # ✅ real SubjectDb
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
    selected_date = request.GET.get("date")
    selected_subject = request.GET.get("subject")
    department = request.GET.get("department")
    semester = request.GET.get("semester")

    subjects = SubjectDb.objects.all()
    records = None

    if selected_date and selected_subject and department and semester:
        records = AttendanceDb.objects.filter(
            date=selected_date,
            subject_id=selected_subject,
            student__department=department,
            student__semester=semester
        )

    return render(request, "View_attendance.html", {
        "subjects": subjects,
        "records": records,
        "selected_date": selected_date,
        "selected_subject": selected_subject,
        "department": department,
        "semester": semester,
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
    teacher_name = request.session.get("Name")

    assigned_subjects = AssignedSubjectDb.objects.filter(
        teacher=teacher_name
    )

    return render(request, "Upload_marks.html", {
        "assigned_subjects": assigned_subjects
    })




def view_marks(request):
    teacher_id = request.session.get("teacher_id")

    assigned_subjects = AssignedSubjectDb.objects.filter(
        teacher_id=teacher_id
    )

    marks = MarksDb.objects.filter(
        subject__in=assigned_subjects.values_list('subject', flat=True)
    )

    return render(request, "view_marks.html", {
        "marks": marks,
        "assigned_subjects": assigned_subjects,
    })



def edit_marks(request, id):
    mark = MarksDb.objects.get(id=id)
    return render(request, "Edit_Marks.html", {"mark": mark})

def update_marks(request, id):
    mark = MarksDb.objects.get(id=id)
    if request.method == "POST":
        mark.exam_type = request.POST.get("exam_type")
        mark.marks = request.POST.get("marks")
        mark.save()
        return redirect("teacherapp:view_marks")

def upload_assignments(request):
    teacher_id = request.session.get("teacher_id")

    assigned_subjects = AssignedSubjectDb.objects.filter(teacher=teacher_id)

    assignments = AssignmentDb.objects.filter(teacher_id=teacher_id).order_by('-id')

    return render(request, "upload_assignments.html", {
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

        AssignmentDb.objects.create(
            teacher_id=teacher_id,
            subject_id=subject_id,
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

def student_profile(request, student_id):
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

from django.shortcuts import render,redirect
from Adminapp.models import SubjectDb,AssignedSubjectDb,StudentDb,TeacherDb
from teacherapp.models import AttendanceDb,MarksDb,AssignmentDb,AssignmentSubmissionDb
from datetime import date
from django.contrib import messages
from django.db.models import Q

from django.utils import timezone


# Create your views here.
def teacher_page(request):
    return render(request, "teacher_index.html")
def teacher_assigned_subjects(request):
    teacher_name = request.session.get("teacher_name")
    data = AssignedSubjectDb.objects.filter(teacher=teacher_name)
    return render(request, 'teacher_assigned_subjects.html', {'data': data})
def view_subjects(request):
    teacher_name = request.session.get('teacher_name')
    print("Teacher session:", teacher_name)

    # Filter the assigned subjects
    data = AssignedSubjectDb.objects.filter(teacher=teacher_name).select_related('subject')

    return render(request, "View_subjects.html", {"data": data})
    # data = SubjectDb.objects.all()
    # return render(request, "View_Subjects.html", {"data": data})
def search_subjects(request):
    teacher = request.session.get("teacher_name")

    # Only show subjects assigned to THIS teacher
    qs = AssignedSubjectDb.objects.filter(teacher=teacher).select_related('subject')

    query = request.GET.get("q")

    if query:
        qs = qs.filter(
            Q(subject__subject_name__icontains=query) |
            Q(subject__subject_code__icontains=query)
        )

    return render(request, "search_subjects.html", {
        "data": qs,
        "query": query
    })


def teacher_dashboard(request):
    if 'Name' in request.session:
        return render(request, 'teacher_index.html')
    else:
        return redirect('teacher_log_in')

def mark_attendance(request):
    teacher_name = request.session.get('Name')
    assigned_subjects = AssignedSubjectDb.objects.filter(teacher=teacher_name)
    class_name = request.GET.get("class")
    subject_id = request.GET.get("subject")
    students = None

    if class_name and subject_id:
        students = StudentDb.objects.filter(student_class=class_name)

    return render(request, "Mark_attendance.html", {
        "assigned_subjects": assigned_subjects,
        "students": students,
        "selected_class": class_name,
        "selected_subject": subject_id,
        "today": date.today(),
    })

def save_attendance(request):
    if request.method == "POST":
        subject_id = request.POST.get("subject_id")
        class_name = request.POST.get("class_name")
        curr_date = request.POST.get("date")

        assigned_subject = AssignedSubjectDb.objects.get(id=subject_id)

        for key, value in request.POST.items():
            if key.startswith("student_"):
                student_id = key.split("_")[1]
                status = value
                AttendanceDb.objects.create(
                    student_id=student_id,
                    assigned_subject=assigned_subject,
                    date=curr_date,
                    status=status
                )

        return redirect("mark_attendance")

def view_attendance(request):
    selected_date = request.GET.get("date")
    selected_subject = request.GET.get("subject")
    selected_class = request.GET.get("class")

    subjects = SubjectDb.objects.all()
    records = None

    if selected_date and selected_subject and selected_class:
        records = AttendanceDb.objects.filter(
            date=selected_date,
            subject_id=selected_subject,
            class_name=selected_class
        )

    return render(request, "View_attendance.html", {
        "subjects": subjects,
        "records": records,
        "selected_date": selected_date,
        "selected_subject": selected_subject,
        "selected_class": selected_class,
    })

def teacher_attendance_report(request):
    teacher_name = request.session.get('Name')

    # Load only subjects assigned to the logged-in teacher
    assigned_subjects = AssignedSubjectDb.objects.filter(teacher=teacher_name)

    selected_subject = request.GET.get('subject')
    selected_class = request.GET.get('class')
    selected_date = request.GET.get('date')

    attendance_data = None

    # Load attendance only when filters are selected
    if selected_subject and selected_class and selected_date:
        attendance_data = AttendanceDb.objects.filter(
            subject_id=selected_subject,
            class_name=selected_class,
            date=selected_date
        )

    return render(request, "Teacher_Attendance_Report.html", {
        "assigned_subjects": assigned_subjects,
        "selected_subject": selected_subject,
        "selected_class": selected_class,
        "selected_date": selected_date,
        "attendance_data": attendance_data,
    })

def upload_marks(request):
    teacher_name = request.session.get("teacher_name")
    assigned_subjects = AssignedSubjectDb.objects.filter(teacher=teacher_name)
    selected_subject = request.GET.get("subject")
    selected_exam = request.GET.get("exam")
    students = None

    if selected_subject and selected_exam:
        subject_obj = AssignedSubjectDb.objects.get(id=selected_subject)
        class_name = subject_obj.class_name

        # Load students of that class
        students = StudentDb.objects.filter(Class=class_name)

    return render(request, "Upload_marks.html", {
        "assigned_subjects": assigned_subjects,
        "selected_subject": selected_subject,
        "selected_exam": selected_exam,
        "students": students,
    })

def view_marks(request):
    teacher_name = request.session.get("teacher_name")

    # Fetch subjects assigned to this teacher
    assigned_subjects = AssignedSubjectDb.objects.filter(teacher=teacher_name)

    # Get marks only for subjects of this teacher
    marks = MarksDb.objects.filter(subject__in=[s.subject for s in assigned_subjects])

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
    teacher_id = request.session.get("teacher_id")

    # Get subjects assigned to this teacher
    assigned_subjects = SubjectDb.objects.filter(teacher=teacher_id)

    # Extract department and semester from assigned subjects
    departments = assigned_subjects.values_list("department", flat=True).distinct()
    semesters = assigned_subjects.values_list("semester", flat=True).distinct()

    # Fetch students matching department & semester
    students = StudentDb.objects.filter(
        department__in=departments,
        semester__in=semesters
    )

    return render(request, "View_Students.html", {
        "students": students,
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

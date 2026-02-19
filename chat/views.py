from django.shortcuts import render, redirect, get_object_or_404
from Adminapp.models import StudentDb, TeacherDb,AssignedSubjectDb
from chat.models import ChatMessageDb
from django.db.models import Q


# Create your views here.
def teacher_chat_students(request):
    teacher_id = request.session.get("teacher_id")
    if not teacher_id:
        return redirect("teacher_log_in")

    teacher = TeacherDb.objects.get(id=teacher_id)

    # Restrict students by department + semester
    assigned_subjects = AssignedSubjectDb.objects.filter(teacher=teacher)
    students = StudentDb.objects.none()

    if assigned_subjects.exists():
        for subject in assigned_subjects:
            department = subject.class_name.split()[0].strip()

            students = students | StudentDb.objects.filter(
                department=department,
                semester=subject.semester
            )

        students = students.distinct()

    selected_student_id = request.GET.get("student_id")
    messages = []

    if selected_student_id:
        student = get_object_or_404(StudentDb, id=selected_student_id)

        # 🔥 Correct conversation filter
        messages = ChatMessageDb.objects.filter(
            Q(sender_teacher=teacher, sender_student__isnull=True) |
            Q(sender_student=student, sender_teacher__isnull=True)
        ).order_by("timestamp")

    return render(request, "teacher_chat.html", {
        "students": students,
        "messages": messages,
        "selected_student_id": selected_student_id,
        "teacher": teacher,
    })


# ===============================
# TEACHER SEND MESSAGE
# ===============================
def teacher_send_message(request):
    if request.method == "POST":
        teacher = TeacherDb.objects.get(id=request.session["teacher_id"])
        student = StudentDb.objects.get(id=request.POST["student_id"])

        # 🔥 Teacher sends → student field NULL
        ChatMessageDb.objects.create(
            sender_teacher=teacher,
            sender_student=None,
            message=request.POST["message"]
        )

        return redirect(f"/chat/teacher_chat_students/?student_id={student.id}")


# ===============================
# STUDENT CHAT VIEW
# ===============================
def student_chat_teacher(request):
    student_id = request.session.get("student_id")
    if not student_id:
        return redirect("student_log_in")

    student = StudentDb.objects.get(id=student_id)

    assigned_subject = AssignedSubjectDb.objects.filter(
        class_name__icontains=student.department,
        semester=student.semester
    ).first()

    if not assigned_subject:
        return render(request, "student_chat.html", {
            "messages": [],
            "teacher": None,
        })

    teacher = TeacherDb.objects.get(name=assigned_subject.teacher)

    # 🔥 Correct conversation filter
    messages = ChatMessageDb.objects.filter(
        Q(sender_teacher=teacher, sender_student__isnull=True) |
        Q(sender_student=student, sender_teacher__isnull=True)
    ).order_by("timestamp")

    return render(request, "student_chat.html", {
        "messages": messages,
        "teacher": teacher,
    })


# ===============================
# STUDENT SEND MESSAGE
# ===============================
def student_send_message(request):
    if request.method == "POST":
        student = StudentDb.objects.get(id=request.session["student_id"])
        teacher = TeacherDb.objects.get(id=request.POST["teacher_id"])

        # 🔥 Student sends → teacher field NULL
        ChatMessageDb.objects.create(
            sender_teacher=None,
            sender_student=student,
            message=request.POST["message"]
        )

        return redirect("chat:student_chat_teacher")









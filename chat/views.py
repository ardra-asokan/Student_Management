from django.shortcuts import render, redirect, get_object_or_404
from Adminapp.models import StudentDb, TeacherDb
from chat.models import ChatMessageDb
from django.db.models import Q


# Create your views here.
def teacher_chat_students(request):
    teacher_id = request.session.get("teacher_id")
    if not teacher_id:
        return redirect("teacher_log_in")

    teacher = TeacherDb.objects.get(id=teacher_id)
    students = StudentDb.objects.all()

    selected_student_id = request.GET.get("student_id")
    messages = []

    if selected_student_id:
        student = StudentDb.objects.get(id=selected_student_id)

        messages = ChatMessageDb.objects.filter(
            sender_student=student
        ).filter(
            Q(sender_teacher=teacher) | Q(sender_teacher__isnull=True)
        ).order_by("timestamp")

    return render(request, "teacher_chat.html", {
        "students": students,
        "messages": messages,
        "selected_student_id": selected_student_id,
        "teacher": teacher,
    })


def teacher_send_message(request):
    if request.method == "POST":
        teacher = TeacherDb.objects.get(id=request.session["teacher_id"])
        student = StudentDb.objects.get(id=request.POST["student_id"])

        ChatMessageDb.objects.create(
            sender_teacher=teacher,
            sender_student=student,
            message=request.POST["message"]
        )

        return redirect(f"/chat/teacher_chat_students/?student_id={student.id}")


def student_chat_teacher(request):
    student_id = request.session.get("student_id")
    if not student_id:
        return redirect("student_log_in")

    student = StudentDb.objects.get(id=student_id)

    # find teacher who chats with this student
    teacher = ChatMessageDb.objects.filter(
        sender_student=student
    ).values_list("sender_teacher", flat=True).first()

    if not teacher:
        return render(request, "student_chat.html", {
            "messages": [],
            "teacher": None,
        })

    teacher = TeacherDb.objects.get(id=teacher)

    messages = ChatMessageDb.objects.filter(
        Q(sender_teacher=teacher, sender_student__isnull=True) |
        Q(sender_student=student, sender_teacher__isnull=True)
    ).order_by("timestamp")

    return render(request, "student_chat.html", {
        "messages": messages,
        "teacher": teacher,
    })


def student_send_message(request):
    if request.method == "POST":
        student = StudentDb.objects.get(id=request.session["student_id"])
        teacher = TeacherDb.objects.get(id=request.POST["teacher_id"])

        ChatMessageDb.objects.create(sender_teacher=None, sender_student=student,message=request.POST["message"])
        return redirect("chat:student_chat_teacher")






from django.urls import path
from chat import views

app_name = "chat"

urlpatterns = [
    path("teacher_chat_students/", views.teacher_chat_students, name="teacher_chat_students"),
    path("teacher_send_message", views.teacher_send_message, name="teacher_send_message"),

    path("student_chat_teacher/", views.student_chat_teacher, name="student_chat_teacher"),
    path("student_send_message/", views.student_send_message, name="student_send_message"),
]
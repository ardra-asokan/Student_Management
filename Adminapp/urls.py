from django.urls import path, include
from mainapp import views as main_views
from Adminapp import views as admin_views


urlpatterns = [
    path('index_page/',admin_views.index_page,name="index_page"),
    path('dashboard/', admin_views.dashboard, name='admin_dashboard'),

    # STUDENT
    path('add_student/',admin_views.add_student,name="add_student"),
    path('view_students/', admin_views.view_students, name='view_students'),
    path('save_student/', admin_views.save_student, name='save_student'),
    path('edit_student/<int:student_id>/', admin_views.edit_student, name='edit_student'),
    path('update_student/<int:s_id>/', admin_views.update_student, name='update_student'),
    path('delete_student/<int:st_id>/', admin_views.delete_student, name='delete_student'),

    # TEACHER
    path('add_teacher/',admin_views.add_teacher,name="add_teacher"),
    path('view_teachers/', admin_views.view_teachers, name='view_teachers'),
    path('save_teacher/', admin_views.save_teacher, name='save_teacher'),
    path('edit_teacher/<int:teacher_id>/', admin_views.edit_teacher, name='edit_teacher'),
    path('update_teacher/<int:t_id>/', admin_views.update_teacher, name='update_teacher'),
    path('delete_teacher/<int:tr_id>/', admin_views.delete_teacher, name='delete_teacher'),




    path('add_subject/',admin_views.add_subject,name="add_subject"),
    path('view_subjects/', admin_views.view_subjects, name='admin_view_subjects'),
    path('save_subject/', admin_views.save_subject, name='admin_save_subject'),
    path('edit_subject/<int:subject_id>/', admin_views.edit_subject, name='edit_subject'),
    path('update_subject/<int:s_id>/', admin_views.update_subject, name='update_subject'),
    path('delete_subject/<int:sub_id>/', admin_views.delete_subject, name='delete_subject'),





    path('assign_teacher/',admin_views.assign_teacher,name="assign_teacher"),
    path('view_assigned_subjects/', admin_views.view_assigned_subjects, name='view_assigned_subjects'),
    path('save_assigned_subject/', admin_views.save_assigned_subject, name='save_assigned_subject'),
    path('edit_assigned_subject/<int:assigned_id>/', admin_views.edit_assigned_subject, name='edit_assigned_subject'),
    path('update_assigned_subject/<int:a_id>/', admin_views.update_assigned_subject, name='update_assigned_subject'),
    path('delete_assigned_subject/<int:as_id>/', admin_views.delete_assigned_subject, name='delete_assigned_subject'),


    path('view_attendance/',admin_views.view_attendance,name="view_attendance"),
    path('attendance_report/',admin_views.attendance_report,name="attendance_report"),
    path('view_marks/',admin_views.view_marks,name="view_marks"),
    path('generate_result/',admin_views.generate_result,name="generate_result"),
    path('view_assignment/',admin_views.view_assignment,name="view_assignment"),
    path('student_submission/',admin_views.student_submission,name="student_submission"),
    path('send_notification/',admin_views.send_notification,name="send_notification"),
    path('student_report/',admin_views.student_report,name="student_report"),
    path('attendance_analytics/',admin_views.attendance_analytics,name="attendance_analytics"),
    path('marks_analytics/',admin_views.marks_analytics,name="marks_analytics")

]
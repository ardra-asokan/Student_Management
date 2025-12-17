from django.urls import path
from teacherapp import views as teacher_views

app_name = "teacherapp"

urlpatterns = [
    path('teacher_page/',teacher_views.teacher_page,name="teacher_page"),
    path('view_subjects/',teacher_views.view_subjects,name="teacher_view_subjects"),
    path('search_subjects/',teacher_views.search_subjects,name="search_subjects"),
    path('teacher_dashboard/',teacher_views.teacher_dashboard, name='teacher_dashboard'),
    path('mark_attendance/', teacher_views.mark_attendance, name='mark_attendance'),
    path('save_attendance/', teacher_views.save_attendance, name='save_attendance'),
    path('teacher_view_attendance/', teacher_views.teacher_view_attendance, name='teacher_view_attendance'),
    path('teacher_attendance_report/', teacher_views.teacher_attendance_report, name='teacher_attendance_report'),
    path('upload_marks/', teacher_views.upload_marks, name='upload_marks'),
    path('teacher_view_marks/', teacher_views.teacher_view_marks, name="teacher_view_marks"),
    path('teacher_edit_marks/<int:id>/', teacher_views.teacher_edit_marks, name="teacher_edit_marks"),
    path('update_marks/<int:id>/', teacher_views.update_marks, name="update_marks"),
    path('upload_assignments/', teacher_views.upload_assignments, name="upload_assignments"),
    path('save_assignment/', teacher_views.save_assignment, name="save_assignment"),
    path('student_submissions/', teacher_views.student_submissions, name="student_submissions"),
    path('grade_assignments/', teacher_views.grade_assignments, name="grade_assignments"),
    path('save_assignment_grades/', teacher_views.save_assignment_grades, name="save_assignment_grades"),
    path('view_students/', teacher_views.view_students, name="view_students"),
    path('search_students/', teacher_views.search_students, name="search_students"),
    path('student_profile/<int:student_id>/', teacher_views.student_profile, name="student_profile"),
    path('delete_assignment/<int:assignment_id>/',teacher_views.delete_assignment,name='delete_assignment'),
    path('teacher_send_announcements/', teacher_views.teacher_send_announcements, name='teacher_send_announcements'),
    path('teacher_view_announcements/', teacher_views.teacher_view_announcements, name='teacher_view_announcements'),
    path('upload_study_material/', teacher_views.upload_study_material, name='upload_study_material'),
    path('teacher_view_study_material/', teacher_views.teacher_view_study_material, name='teacher_view_study_material'),
    path('delete_study_material/<int:material_id>/',teacher_views.delete_study_material,name='delete_study_material'),
    path('student_profile/', teacher_views.student_profile, name='student_profile'),

]
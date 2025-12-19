from django.urls import path
from studentapp import views

app_name = 'studentapp'

urlpatterns = [
    path('student_page/', views.student_page, name='student_page'),
    path('student_profile/', views.student_profile, name='student_profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('view_student_subjects/', views.view_student_subjects, name='view_student_subjects'),
    path('student_subject_details/<int:subject_id>/', views.student_subject_details, name='student_subject_details'),
    path('student_attendance/', views.student_attendance, name='student_attendance'),
    path('student_timetable/', views.student_timetable, name='student_timetable'),
    path('student_internal_marks/', views.student_internal_marks, name='student_internal_marks'),
    path('student_semester_results/', views.student_semester_results, name='student_semester_results'),

    path('student_assignments/', views.student_assignments, name='student_assignments'),
    path('student_notifications/', views.student_notifications, name='student_notifications'),
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),

]
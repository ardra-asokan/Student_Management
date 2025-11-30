from django.urls import path
from studentapp import views

urlpatterns = [
    path('student_page/', views.student_page, name='student_page'),
    path('student_profile/', views.student_profile, name='student_profile'),
    path('student_subjects/', views.student_subjects, name='student_subjects'),
    path('student_attendance/', views.student_attendance, name='student_attendance'),
    path('student_timetable/', views.student_timetable, name='student_timetable'),
    path('student_results/', views.student_results, name='student_results'),
    path('student_assignments/', views.student_assignments, name='student_assignments'),
    path('student_notifications/', views.student_notifications, name='student_notifications'),
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),

]
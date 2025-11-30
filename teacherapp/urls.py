from django.urls import path
from teacherapp import views as teacher_views

urlpatterns = [
    path('teacher_page/',teacher_views.teacher_page,name="teacher_page"),
    path('view_subjects/',teacher_views.view_subjects,name="teacher_view_subjects"),
    path('search_subjects/',teacher_views.search_subjects,name="search_subjects"),
    path('teacher_dashboard/', teacher_views.teacher_dashboard, name='teacher_dashboard'),
]
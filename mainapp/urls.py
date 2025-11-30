from django.urls import path
from mainapp import views

urlpatterns = [
    path('home_page/',views.home_page,name="home_page"),
    path('login/',views.login,name="login"),
    path('sign_up/',views.sign_up,name="sign_up"),
    path('save_signup_data/',views.save_signup_data,name="save_signup_data"),
    path('admin_login/',views.admin_login,name="admin_login"),
    path('admin_logout/',views.admin_logout,name="admin_logout"),
    path('about_page/',views.about_page,name="about_page"),
    path('contact_page/',views.contact_page,name="contact_page"),
    path('login_page/',views.login_page,name="login_page"),

    path('teacher_log_in/',views.teacher_log_in,name="teacher_log_in"),
    path('teacher_sign_up/',views.teacher_sign_up,name="teacher_sign_up"),
    path('save_teacher_signup_data/',views.save_teacher_signup_data,name="save_teacher_signup_data"),
    path('teacher_login/',views.teacher_login,name="teacher_login"),
    path('teacher_logout/',views.teacher_logout,name="teacher_logout"),

    path('student_log_in/',views.student_log_in,name="student_log_in"),
    path('student_sign_up/',views.student_sign_up,name="student_sign_up"),
    path('save_student_signup_data/',views.save_student_signup_data,name="save_student_signup_data"),
    path('student_login/',views.student_login,name="student_login"),
    path('student_logout/',views.student_logout,name="student_logout"),

]

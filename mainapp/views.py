from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from mainapp.models import SignupDb
from Adminapp.models import TeacherDb,StudentDb


# Create your views here.
def home_page(request):
    return render(request,"Home.html")
def about_page(request):
    return render(request,"About.html")
def contact_page(request):
    return render(request,"Contact.html")
def login_page(request):
    return render(request,"LoginPage.html")


def login(request):
    return render(request, "Login.html")
def sign_up(request):
    return render(request, "Sign_up.html")

def save_signup_data(request):
    if request.method == "POST":
        nm = request.POST.get('name')
        em = request.POST.get('email')
        ps = request.POST.get('password')
        cps = request.POST.get('cpassword')
        obj = SignupDb(Name=nm, Email=em, Password=ps, Confirm_Password=cps)
        if SignupDb.objects.filter(Name=nm).exists():
            # Alert-Username already exists..!
            return redirect(sign_up)
        elif SignupDb.objects.filter(Email=em).exists():
            # Alert-Email already exists..!
            return redirect(sign_up)
        else:
            obj.save()
            return redirect(login)

def admin_login(request):
    if request.method == "POST":
        un = request.POST.get('username')
        pswd = request.POST.get('password')
        if SignupDb.objects.filter(Name=un,Password=pswd).exists():
            request.session['Name']=un
            request.session['Password'] = pswd
            return redirect('admin_dashboard')
        else:
            return redirect(login)
    else:
        return redirect(login)

def admin_logout(request):
    del request.session['Name']
    del request.session['Password']
    return redirect(login)



# TEACHER LOGIN
def teacher_log_in(request):
    return render(request, "Teacher_Login.html")



def teacher_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            teacher = TeacherDb.objects.get(
                username=username,
                password=password
            )

            request.session['teacher_id'] = teacher.id
            request.session['teacher_name'] = teacher.name

            return redirect('teacherapp:teacher_dashboard')

        except TeacherDb.DoesNotExist:
            return redirect('teacher_log_in')

    return redirect('teacher_log_in')


def teacher_logout(request):
    request.session.flush()
    return redirect('teacher_log_in')


# STUDENT LOGIN

def student_log_in(request):
    return render(request, "Student_Login.html")

def student_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            student = StudentDb.objects.get(
                username=username,
                password=password
            )

            request.session['student_id'] = student.id
            request.session['student_name'] = student.name

            return redirect('student_dashboard')

        except StudentDb.DoesNotExist:
            return redirect('student_log_in')

    return redirect('student_log_in')


def student_logout(request):
    request.session.flush()
    return redirect(student_log_in)


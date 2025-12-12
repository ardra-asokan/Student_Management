from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from mainapp.models import SignupDb,TeacherSignUpDb,StudentSignUpDb
from Adminapp.models import TeacherDb


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
def teacher_sign_up(request):
    return render(request, "Teacher_signup.html")

def save_teacher_signup_data(request):
    if request.method == "POST":
        nm = request.POST.get('name')
        em = request.POST.get('email')
        ps = request.POST.get('password')
        cps = request.POST.get('cpassword')
        obj = TeacherSignUpDb(Name=nm, Email=em, Password=ps, Confirm_Password=cps)
        if TeacherSignUpDb.objects.filter(Name=nm).exists():
            # Alert-Username already exists..!
            return redirect(teacher_sign_up)
        elif TeacherSignUpDb.objects.filter(Email=em).exists():
            # Alert-Email already exists..!
            return redirect(teacher_sign_up)
        else:
            obj.save()
            return redirect(teacher_log_in)

def teacher_login(request):
    if request.method == "POST":
        un = request.POST.get('username')
        pswd = request.POST.get('password')
        if TeacherSignUpDb.objects.filter(Name=un,Password=pswd).exists():
            request.session['Name']=un
            request.session['Password'] = pswd
            if TeacherSignUpDb.objects.filter(Name=un, Password=pswd).exists():
                teacher = TeacherSignUpDb.objects.get(Name=un, Password=pswd)


                request.session['teacher_name'] = teacher.Name


            return redirect('teacherapp:teacher_dashboard')
        else:
            return redirect(teacher_log_in)
    else:
        return redirect(teacher_log_in)

def teacher_logout(request):
    del request.session['Name']
    del request.session['Password']
    return redirect(teacher_login)


# STUDENT LOGIN

def student_log_in(request):
    return render(request, "Student_Login.html")
def student_sign_up(request):
    return render(request, "Student_signup.html")

def save_student_signup_data(request):
    if request.method == "POST":
        nm = request.POST.get('name')
        em = request.POST.get('email')
        ps = request.POST.get('password')
        cps = request.POST.get('cpassword')
        obj = StudentSignUpDb(Name=nm, Email=em, Password=ps, Confirm_Password=cps)
        if StudentSignUpDb.objects.filter(Name=nm).exists():
            # Alert-Username already exists..!
            return redirect(teacher_sign_up)
        elif StudentSignUpDb.objects.filter(Email=em).exists():
            # Alert-Email already exists..!
            return redirect(student_sign_up)
        else:
            obj.save()
            return redirect(student_log_in)

def student_login(request):
    if request.method == "POST":
        un = request.POST.get('username')
        pswd = request.POST.get('password')
        if StudentSignUpDb.objects.filter(Name=un,Password=pswd).exists():
            request.session['Name']=un
            request.session['Password'] = pswd
            return redirect('student_dashboard')
        else:
            return redirect(student_log_in)
    else:
        return redirect(student_log_in)

def student_logout(request):
    del request.session['Name']
    del request.session['Password']
    return redirect(student_login)


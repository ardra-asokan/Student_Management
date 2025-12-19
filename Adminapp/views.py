from django.shortcuts import render,redirect
from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import MultiValueDictKeyError
from Adminapp.models import StudentDb,TeacherDb,SubjectDb,AssignedSubjectDb,AnnouncementDb
from django.contrib import messages


# Create your views here.
def index_page(request):
    return render(request, "index.html")


def add_student(request):
    return render(request,"Add_Student.html")
def view_students(request):
    data = StudentDb.objects.all()
    return render(request, "Student_Details.html", {'data': data})
def save_student(request):
    if request.method == "POST":
        name = request.POST.get('name')
        roll_no = request.POST.get('roll_no')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        department = request.POST.get('department')
        semester = request.POST.get('semester')
        batch = request.POST.get('batch')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        img = request.FILES['profile_photo']
        obj = StudentDb(name=name,roll_no=roll_no,dob=dob,gender=gender,email=email,phone=phone,department=department,semester=semester,batch=batch,username=username,password=password,address=address,profile_photo=img)
        obj.save()
        return redirect('Adminapp:add_student')
def edit_student(request, student_id):
    student = StudentDb.objects.get(id=student_id)
    return render(request, "Edit_Student.html", {'student': student})
def update_student(request, s_id):
    if request.method == "POST":
        name = request.POST.get('name'),
        roll_no = request.POST.get('roll_no'),
        dob = request.POST.get('dob'),
        gender = request.POST.get('gender'),
        email = request.POST.get('email'),
        phone = request.POST.get('phone'),
        department = request.POST.get('department'),
        semester = request.POST.get('semester'),
        batch = request.POST.get('batch'),
        username = request.POST.get('username'),
        password = request.POST.get('password'),
        address = request.POST.get('address'),

        try:
            img = request.FILES['image']
            fs = FileSystemStorage()
            file = fs.save(img.name, img)
        except MultiValueDictKeyError:
            file = StudentDb.objects.get(id=s_id).profile_photo
        StudentDb.objects.filter(id=s_id).update(name=name,roll_no=roll_no,dob=dob,gender=gender,email=email,phone=phone,department=department,semester=semester,batch=batch,username=username,password=password,address=address,profile_photo=file)
        return redirect('Adminapp:view_students')

def delete_student(request, st_id):
    data = StudentDb.objects.filter(id=st_id)
    data.delete()
    return redirect('Adminapp:view_students')


    # TEACHER
def add_teacher(request):
    return render(request,"Add_Teacher.html")
def view_teachers(request):
    data = TeacherDb.objects.all()
    return render(request, "Teacher_Details.html", {'data': data})
def save_teacher(request):
    if request.method == "POST":
        name = request.POST.get('name')
        employee_id = request.POST.get('employee_id')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        department = request.POST.get('department')
        qualification = request.POST.get('qualification')
        experience = request.POST.get('experience')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        img = request.FILES['profile_photo']

        obj = TeacherDb(name=name,employee_id=employee_id,dob=dob,gender=gender,email=email,phone=phone,department=department,qualification=qualification,experience=experience,username=username,password=password,address=address,profile_photo=img)
        obj.save()
        return redirect('Adminapp:add_teacher')
def edit_teacher(request, teacher_id):
    teacher = TeacherDb.objects.get(id=teacher_id)
    return render(request, "Edit_Teacher.html", {'teacher': teacher})
def update_teacher(request, t_id):
    if request.method == "POST":
        name = request.POST.get('name')
        employee_id = request.POST.get('employee_id')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        department = request.POST.get('department')
        qualification = request.POST.get('qualification')
        experience = request.POST.get('experience')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')


        try:
            img = request.FILES['image']
            fs = FileSystemStorage()
            file = fs.save(img.name, img)
        except MultiValueDictKeyError:
            file = TeacherDb.objects.get(id=t_id).profile_photo
        TeacherDb.objects.filter(id=t_id).update(name=name,employee_id=employee_id,dob=dob,gender=gender,email=email,phone=phone,department=department,qualification=qualification,experience=experience,username=username,password=password,address=address,profile_photo=file)
        return redirect('Adminapp:view_teachers')
def delete_teacher(request, tr_id):
    data = TeacherDb.objects.filter(id=tr_id)
    data.delete()
    return redirect('Adminapp:view_teachers')





def add_subject(request):
    teachers = TeacherDb.objects.all()
    return render(request,"Add_Subjects.html", {'teachers': teachers} )
def view_subjects(request):
    data = SubjectDb.objects.all()
    return render(request, "Subject_Details.html", {'data': data})
def save_subject(request):
    if request.method == "POST":
        subject_name = request.POST.get('subject_name')
        subject_code = request.POST.get('subject_code')
        department = request.POST.get('department')
        semester = request.POST.get('semester')
        teacher_id = request.POST.get('teacher')
        teacher = TeacherDb.objects.get(id=teacher_id)
        obj = SubjectDb(subject_name=subject_name,subject_code=subject_code,department=department,semester=semester,teacher=teacher)
        obj.save()
        return redirect('Adminapp:admin_view_subjects')
def edit_subject(request, subject_id):
    subject = SubjectDb.objects.get(id=subject_id)
    teachers = TeacherDb.objects.all()
    return render(request, "Edit_Subjects.html", {'subject': subject, 'teachers': teachers})
def update_subject(request, s_id):
    if request.method == "POST":
        name = request.POST.get('name')
        code = request.POST.get('code')
        semester = request.POST.get('semester')
        teacher_id = request.POST.get('teacher')
        teacher = TeacherDb.objects.get(id=teacher_id)
        SubjectDb.objects.filter(id=s_id).update(subject_name=name,subject_code=code,teacher=teacher,semester=semester)
        return redirect('Adminapp:admin_view_subjects')
def delete_subject(request, sub_id):
    SubjectDb.objects.filter(id=sub_id).delete()
    return redirect('Adminapp:admin_view_subjects')


# # Add Assigned Subject Page
# def add_assigned_subject(request):
#     teachers = TeacherDb.objects.all()
#     subjects = SubjectDb.objects.all()
#     return render(request, "Add_Assigned_Subject.html", {'teachers': teachers, 'subjects': subjects})


# def view_assigned_subjects(request):
#     data = AssignedSubjectDb.objects.all()
#     teachers = TeacherDb.objects.all()
#     return render(request, "Assigned_Subjects.html", {'data': data, 'teachers': teachers})


# Add Assigned Subject to teachers
def assign_teacher(request):
    teachers = TeacherDb.objects.all()
    subjects = SubjectDb.objects.all()
    return render(request,"Assign_Teacher.html", {'teachers': teachers, 'subjects': subjects})

def view_assigned_subjects(request):
    data = AssignedSubjectDb.objects.all()
    teachers = TeacherDb.objects.all()
    return render(request, "AssignedSub_Details.html", {'data': data, 'teachers': teachers})

def save_assigned_subject(request):
    if request.method == "POST":
        teacher_name = request.POST.get('teacher')
        subject_name = request.POST.get('subject')
        class_name = request.POST.get('class')
        semester = request.POST.get('semester')

        teacher = TeacherDb.objects.get(name=teacher_name)
        subject = SubjectDb.objects.get(subject_name=subject_name)

        obj = AssignedSubjectDb(teacher=teacher,subject=subject,class_name=class_name,semester=semester)
        obj.save()
        return redirect('Adminapp:view_assigned_subjects')



def edit_assigned_subject(request, assign_id):
    assigned = AssignedSubjectDb.objects.get(id=assign_id)
    teachers = TeacherDb.objects.all()
    subjects = SubjectDb.objects.all()

    return render(request, "Edit_Assigned_Subject.html", {'assigned': assigned,'teachers': teachers, 'subjects': subjects, 'assigned_subject': assigned.subject,})


def update_assigned_subject(request, a_id):
    if request.method == "POST":
        teacher_name = request.POST.get('teacher')
        subject_name = request.POST.get('subject')
        class_name = request.POST.get('class')
        semester = request.POST.get('semester')

        teacher = TeacherDb.objects.get(name=teacher_name)
        subject = SubjectDb.objects.get(subject_name=subject_name)

        AssignedSubjectDb.objects.filter(id=a_id).update(
            teacher=teacher,
            subject=subject,
            class_name=class_name,
            semester=semester
        )

        return redirect('Adminapp:view_assigned_subjects')


def delete_assigned_subject(request, as_id):
    AssignedSubjectDb.objects.filter(id=as_id).delete()
    return redirect('Adminapp:view_assigned_subjects')


def admin_view_attendance(request):
    subjects = SubjectDb.objects.all()
    return render(request,"View_Attendance.html", {"subjects": subjects})
def attendance_report(request):
    return render(request,"Attendance_Report.html")
def view_marks(request):
    return render(request,"View_Marks.html")
def generate_result(request):
    return render(request,"Generate_Result.html")
def view_assignment(request):
    teachers = TeacherDb.objects.all()
    subjects = SubjectDb.objects.all()
    return render(request,"View_TeacherAssignment.html", {"teachers": teachers, "subjects":subjects} )
def student_submission(request):
    return render(request,"Student_Submission.html")
def send_announcement(request):
    admin_name = request.session.get("admin_name")  # adjust if your session key differs

    if request.method == "POST":
        title = request.POST.get("title")
        message = request.POST.get("message")

        AnnouncementDb.objects.create(
            title=title,
            message=message,
            sender_type="Admin",
            sender_name=admin_name if admin_name else "Admin"
        )

        messages.success(request, "Announcement sent successfully")
        return redirect("Adminapp:send_announcement")



def view_teacher_announcements(request):
    announcements = AnnouncementDb.objects.filter(
        sender_type="Teacher"
    ).order_by('-created_at')

    return render(request, "View_Announcements.html", {
        "announcements": announcements
    })


def student_report(request):
    return render(request, "Student_Report.html")
def attendance_analytics(request):
    return render(request,"Attendance_Analytics.html")
def marks_analytics(request):
    return render(request,"Marks_Analytics.html")


def dashboard(request):
    if 'Name' in request.session:  # Optional: check if admin is logged in
        return render(request, 'index.html')
    else:
        return redirect('login')

from django.shortcuts import render,get_object_or_404,redirect
from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import MultiValueDictKeyError
from Adminapp.models import *
from django.contrib import messages
from teacherapp.models import AttendanceDb,MarksDb,AssignmentDb,AssignmentSubmissionDb
from datetime import datetime
from django.http import HttpResponse
from reportlab.pdfgen import canvas


# Create your views here.
def index_page(request):

    teacher_count = TeacherDb.objects.count()
    student_count = StudentDb.objects.count()
    subject_count = SubjectDb.objects.count()

    total_assignments = AssignmentDb.objects.count()
    submitted_assignments = AssignmentSubmissionDb.objects.count()

    if total_assignments > 0:
        assignment_percent = int((submitted_assignments / total_assignments) * 100)
    else:
        assignment_percent = 0

    teacher_announcements = AnnouncementDb.objects.filter(
        sender_type="Teacher"
    ).order_by("-created_at")[:5]

    return render(request, "index.html", {
        "teacher_count": teacher_count,
        "student_count": student_count,
        "subject_count": subject_count,
        "assignment_percent": assignment_percent,
        "teacher_announcements": teacher_announcements,
        "teacher_announcement_count": teacher_announcements.count()
    })


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




    # SUBJECT
def add_subject(request):
    teachers = TeacherDb.objects.all()
    return render(request,"Add_Subjects.html", {'teachers': teachers} )
def view_subjects(request):
    data = SubjectDb.objects.all()
    return render(request, "Student_Subject_Details.html", {'data': data})
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
    attendance = None

    if request.method == "POST":
        att_date = request.POST.get("att_date")
        subject_id = request.POST.get("subject")

        if att_date and subject_id:
            try:
                att_date = datetime.strptime(att_date, "%Y-%m-%d").date()
                attendance = AttendanceDb.objects.filter(
                    date=att_date,
                    subject_id=subject_id
                )
            except ValueError:
                attendance = None

    return render(request, "View_Attendance.html", {
        "subjects": subjects,
        "attendance": attendance
    })


def attendance_report(request):
    reports = None

    from_date = request.GET.get("from_date")
    to_date = request.GET.get("to_date")
    department = request.GET.get("department")
    semester = request.GET.get("semester")

    print(from_date, to_date, department, semester)  # DEBUG

    if from_date and to_date and department and semester:
        from_date = datetime.strptime(from_date, "%Y-%m-%d").date()
        to_date = datetime.strptime(to_date, "%Y-%m-%d").date()

        reports = AttendanceDb.objects.filter(date__range=(from_date, to_date), student__department=department, student__semester=semester.select_related("student", "subject"))

        if not reports.exists():
            reports = None

    return render(request, "Attendance_Report.html", {
        "reports": reports
    })



def view_marks(request):
    marks = None
    roll_no = request.GET.get('roll_no')
    semester = request.GET.get('semester')

    if roll_no and semester:
        marks = MarksDb.objects.filter(
            student__roll_no=roll_no,
            student__semester=semester
        ).select_related('student', 'subject')

    return render(request, 'View_Marks.html', {
        'marks': marks,
        'roll_no': roll_no,
        'semester': semester,
    })


def generate_result(request):
    roll_no = request.GET.get("roll_no")

    if not roll_no:
        return render(request, "Generate_Result.html")

    student = StudentDb.objects.filter(roll_no=roll_no).first()
    marks = MarksDb.objects.filter(student__roll_no=roll_no)

    if not student or not marks.exists():
        return HttpResponse("No result found")

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{roll_no}_result.pdf"'

    p = canvas.Canvas(response)
    y = 800

    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, y, "Student Result")
    y -= 40

    p.setFont("Helvetica", 12)
    p.drawString(50, y, f"Name: {student.name}")
    y -= 20
    p.drawString(50, y, f"Roll No: {student.roll_no}")
    y -= 20
    p.drawString(50, y, f"Semester: {student.semester}")
    y -= 30

    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y, "Subject")
    p.drawString(250, y, "Exam")
    p.drawString(350, y, "Marks")
    y -= 20

    p.setFont("Helvetica", 12)
    for m in marks:
        p.drawString(50, y, m.subject.subject_name)
        p.drawString(250, y, m.exam_type)
        p.drawString(350, y, str(m.marks))
        y -= 20

        if y < 50:
            p.showPage()
            y = 800

    p.showPage()
    p.save()

    return response


def view_teacher_assignment(request):
    teachers = TeacherDb.objects.all()
    subjects = SubjectDb.objects.all()
    assignments = None

    teacher_id = request.GET.get("teacher")
    subject_id = request.GET.get("subject")

    if teacher_id and subject_id:
        assignments = AssignmentDb.objects.filter(teacher_id=teacher_id, subject_id=subject_id).select_related("teacher", "subject")

    return render(request,"View_TeacherAssignment.html",{
            "teachers": teachers,
            "subjects": subjects,
            "assignments": assignments,
            "selected_teacher": teacher_id,
            "selected_subject": subject_id,
        }
    )

def student_submission(request):
    assignments = AssignmentDb.objects.all()
    submissions = None

    assignment_id = request.GET.get("assignment")

    if assignment_id:
        submissions = AssignmentSubmissionDb.objects.filter(assignment_id=assignment_id).select_related("student", "assignment")

    return render(request,"Student_Submission.html",{
            "assignments": assignments,
            "submissions": submissions,
            "selected_assignment": assignment_id,
        })
def send_announcement(request):
    admin_name = request.session.get("admin_name")  # session value

    if request.method == "POST":
        title = request.POST.get("title")
        message = request.POST.get("message")

        if title and message:
            AnnouncementDb.objects.create(
                title=title,
                message=message,
                sender_type="Admin",
                sender_name=admin_name if admin_name else "Admin"
            )

            messages.success(request, "Announcement sent successfully")
            return redirect("Adminapp:send_announcement")
        else:
            messages.error(request, "All fields are required")
    return render(request, "Admin_Send_Announcement.html")



def view_teacher_announcements(request):
    announcements = AnnouncementDb.objects.filter(
        sender_type="Teacher").order_by('-created_at')

    return render(request, "View_Announcements.html", {
        "announcements": announcements
    })
def admin_delete_announcement(request, announcement_id):
    if request.method == "POST":
        announcement = get_object_or_404(AnnouncementDb, id=announcement_id)
        announcement.delete()
        messages.success(request, "Announcement deleted successfully")

    return redirect("Adminapp:view_teacher_announcements")



def dashboard(request):
    if 'Name' in request.session:
        return render(request, 'index.html')
    else:
        return redirect('login')

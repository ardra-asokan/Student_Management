from django.shortcuts import render,redirect
from Adminapp.models import SubjectDb

# Create your views here.
def teacher_page(request):
    return render(request, "teacher_index.html")
def view_subjects(request):
    data = SubjectDb.objects.all()
    return render(request, "View_Subjects.html", {"data": data})
def search_subjects(request):
    data = SubjectDb.objects.all()
    return render(request, "Search_Subjects.html", {"data": data})

def teacher_dashboard(request):
    if 'Name' in request.session:
        return render(request, 'teacher_index.html')
    else:
        return redirect('teacher_log_in')


from django.shortcuts import render
from django.http import HttpResponse
from profiles.models import Subject, Student
import json

# Create your views here.
def reportView(request):
    template_name = 'exams/report.html'

    class_choices = (('1', 'Class 1'), ('2', 'Class 2'), ('3', 'Class 3'), ('4', 'Class 4'), ('5', 'Class 5'), ('6', 'Class 6'), ('7', 'Class 7'), ('8', 'Class 8'), ('9', 'Class 9'), ('10', 'Class 10'), ('11', 'Class 11'), ('12', 'Class 12'), ('LKG', 'LKG'), ('UKG', 'UKG'))

    context = {
        'class': class_choices,
        'selected_class': None,
        'selected_subject': None
    }
    if request.method=="POST":
        if request.POST['class'] and request.POST['subject']:
            students = request.user.school.student_set.filter(stud_class=request.POST['class'])
            # students = Student.objects.filter(stud_class=request.POST['class'], student_school)
            context.update({
                'students': students,
                'selected_class': request.POST['class'],
                'selected_subject': request.POST['subject']
            })
        elif request.POST['class']:
            print('please select subject')
        else:
            print('invalid post request')

    return render(request, template_name, context)

def getSubjects(request, class_level):
    subjects = Subject.objects.filter(subject_class=class_level)
    res = {
        'subjects': []
    }
    for subject in subjects:
        res['subjects'].append(subject.subject_name)
    json_res = json.dumps(res)
    return HttpResponse(json_res, content_type="application/json")



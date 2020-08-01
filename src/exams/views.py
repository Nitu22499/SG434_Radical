from django.shortcuts import render
from django.http import HttpResponse

# Importing models
from profiles.models import Subject, Student
from exams.models import Exam

# Importing Libraries
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
        # -- Correct Version (won't work because of the bug)
        #    students = request.user.school.student_set.filter(stud_class=request.POST['class'])
        # ++ Only for testing purpose till the registration bug is resolved
            students = Student.objects.filter(stud_class=request.POST['class'])
            for student in students:
                subject = Subject.objects.get(subject_name=request.POST['subject'])
                if not student.exam_set.filter(subject=subject):
                    Exam.objects.create(student=student, subject=subject)
                student.exam = student.exam_set.get( subject=subject)
            context.update({
                'students': students,
                'selected_class': request.POST['class'],
                'selected_subject': request.POST['subject']
            })
        elif request.POST['class']:
            print('please select subject')
            context.update({
                'error_msg': "Please select a Subject",
                'selected_class': request.POST['class']
            })
        else:
            print('invalid post request')
            context.update({
                'error_msg': "Invalid Request",
            })

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

def saveExamForm(request):
    students = json.loads(request.body)
    for stud in students:
        # print(Exam.objects.get(student=Student.objects.get(user=stud.first_name)))
        try:
            exam_marks = Exam.objects.get(id=stud['id'])
            exam_marks.per_test_1 = stud['test_1'] or None
            exam_marks.per_test_2=stud['test_2'] or None
            exam_marks.main_1=stud['half_yearly_1'] or None
            exam_marks.main_2=stud['half_yearly_2'] or None
            exam_marks.notebook_1=stud['notebook_1'] or None
            exam_marks.notebook_2=stud['notebook_2'] or None
            exam_marks.sea_1=stud['sea_1'] or None
            exam_marks.sea_2=stud['sea_2'] or None
            # exam_marks.update(per_test_1=stud['test_1'] or None,
            #     per_test_2=stud['test_2'] or None,
            #     main_1=stud['half_yearly_1'] or None,
            #     main_2=stud['half_yearly_2'] or None,
            #     notebook_1=stud['notebook_1'] or None,
            #     notebook_2=stud['notebook_2'] or None,
            #     sea_1=stud['sea_1'] or None,
            #     sea_2=stud['sea_2'] or None
            # )
            exam_marks.full_clean()
            exam_marks.save()
        except Exception as e:
            print(e)
            return HttpResponse(json.dumps({ "err": str(e) }), content_type="application/json")

    return HttpResponse(json.dumps({ "msg": "success" }), content_type="application/json")
    


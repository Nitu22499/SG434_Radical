from django.shortcuts import render
from django.http import HttpResponse

# Importing models
from profiles.models import Subject, Student
from exams.models import Exam, ExamCoScholastic

# Importing Libraries
import json

# Importing Utitlities
from misc.utilities import academic_year

# Create your views here.
def reportView(request):
    template_name = 'exams/report.html'

    class_choices = (('1', 'Class 1'), ('2', 'Class 2'), ('3', 'Class 3'), ('4', 'Class 4'), ('5', 'Class 5'), ('6', 'Class 6'), ('7', 'Class 7'), ('8', 'Class 8'), ('9', 'Class 9'), ('10', 'Class 10'), ('11', 'Class 11'), ('12', 'Class 12'), ('LKG', 'LKG'), ('UKG', 'UKG'))

    context = {
        'class': class_choices,
        'selected_class': None,
        'selected_subject': None,
        'academic_year': academic_year()
    }
    if request.method=="POST":
        if request.POST['class'] and request.POST['subject']:
        # -- Correct Version (won't work because of the bug)
        #    students = request.user.school.student_set.filter(stud_class=request.POST['class'])
        # ++ Only for testing purpose till the registration bug is resolved
            students = Student.objects.filter(stud_class=request.POST['class'])
            for student in students:
                subject = Subject.objects.get(subject_name=request.POST['subject'])
                if subject.subject_type == 'Co -Scholastic':
                    if not student.examcoscholastic_set.filter(exam_cs_subject=subject):
                        ExamCoScholastic.objects.create(exam_cs_student=student, exam_cs_subject=subject)
                    student.exam = student.examcoscholastic_set.get(exam_cs_subject=subject)
                    context.update({
                        'has_co_scholastic_subject': True
                    })
                else:
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
            exam_marks.full_clean()
            exam_marks.save()
        except Exception as e:
<<<<<<< HEAD
            return HttpResponse(json.dumps({ "err": str(e) }), content_type="application/json")

    return HttpResponse(json.dumps({ "msg": "success" }), content_type="application/json")

def saveExamFormCoScholastic(request):
    students = json.loads(request.body)
    for stud in students:
        # print(Exam.objects.get(student=Student.objects.get(user=stud.first_name)))
        try:
            exam_marks = ExamCoScholastic.objects.get(id=stud['id'])
            exam_marks.exam_cs_grade_1 = stud['grade_1'] or None
            exam_marks.exam_cs_grade_2=stud['grade_2'] or None

            exam_marks.full_clean()
            exam_marks.save()
        except Exception as e:
=======
>>>>>>> 5f4efb534685bc7d32325b0a9ecec487ebfda2fe
            return HttpResponse(json.dumps({ "err": str(e) }), content_type="application/json")

    return HttpResponse(json.dumps({ "msg": "success" }), content_type="application/json")
    
<<<<<<< HEAD
def studentReportView(request):
    template_name = 'exams/student-report.html'

    # Correct Version ----
    #                    v
    # subjects = Subjects.filter(student=request.user.school.student_set.filter(stud_class=request.POST['class'],stud_section=request.POST['section'],stud_rollno=request.POST['rollno']))
    # Temporary Version ---
    #                     v
    current_student = Student.objects.get(stud_class='10',stud_section='A',stud_rollno='1')
    scholastic_subjects = current_student.exam_set.all()
    context = {
        'subjects': scholastic_subjects,
        'academic_year': academic_year()
    }

    return render(request, template_name, context)
=======
>>>>>>> 5f4efb534685bc7d32325b0a9ecec487ebfda2fe

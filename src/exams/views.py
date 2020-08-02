from django.shortcuts import render
from django.http import HttpResponse
from profiles.models import class_choices, section_choices

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

    context = {
        'class': class_choices,
        'selected_class': None,
        'selected_subject': None,
        'academic_year': academic_year()
    }
    if request.method=="POST":
        if request.POST['class'] and request.POST['subject']:
        # -- Correct Version (won't work because of the bug)
            students = request.user.school.student_set.filter(stud_class=request.POST['class'])
        # ++ Only for testing purpose till the registration bug is resolved
            # students = Student.objects.filter(stud_class=request.POST['class'])
            subject = Subject.objects.get(subject_name=request.POST['subject'],subject_class=request.POST['class'],subject_board=request.user.school.school_board)
            subject_type = subject.subject_type
            if subject_type == "Co -Scholastic":
                context.update({
                    'has_co_scholastic_subject': True
                })
            
            for student in students:
                if subject_type == 'Co -Scholastic':
                    if not student.examcoscholastic_set.filter(exam_cs_subject=subject):
                        ExamCoScholastic.objects.create(exam_cs_student=student, exam_cs_subject=subject)
                    student.exam = student.examcoscholastic_set.get(exam_cs_subject=subject)                    
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
            context.update({
                'error_msg': "Please select a Subject",
                'selected_class': request.POST['class']
            })
        else:
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
            return HttpResponse(json.dumps({ "err": str(e) }), content_type="application/json")

    return HttpResponse(json.dumps({ "msg": "success" }), content_type="application/json")
    
def myReportView(request):
    template_name = 'exams/my-report.html'
    context = {
        'academic_year': academic_year(),
        'school_name': request.user.student.stud_school.school_name
    }
    try:
        current_student = request.user.student
        scholastic_subjects = current_student.exam_set.all()
        co_scholastic_subjects = current_student.examcoscholastic_set.all()
        context.update({
            'subjects': scholastic_subjects,
            'co_subjects': co_scholastic_subjects,
            'student': current_student
        })
    except Exception as e:
        context.update({
            'no_record': True
        })
        return [template_name, context]
    return [template_name, context]


def studentReportView(request):
    if request.user.is_student:
        template_name, context = myReportView(request)
        return render(request, template_name, context)
    else:
        template_name = 'exams/student-report.html'

        sections = [ item for item in section_choices if item[0] ]
        context = {
            'academic_year': academic_year(),
            'class': class_choices,
            'section': sections,
            'school_name': request.user.school.school_name
        }

        if request.method=="POST":
            if request.POST['class'] and request.POST['section'] and request.POST['roll_no']:
                try:
                    current_student = request.user.school.student_set.get(stud_class=request.POST['class'],stud_section=request.POST['section'],stud_rollno=request.POST['roll_no'])
                    scholastic_subjects = current_student.exam_set.all()
                    co_scholastic_subjects = current_student.examcoscholastic_set.all()
                    context.update({
                        'subjects': scholastic_subjects,
                        'co_subjects': co_scholastic_subjects,
                        'selected_class': request.POST['class'],
                        'selected_section': request.POST['section'],
                        'input_rollno': request.POST['roll_no'],
                        'student': current_student
                    })
                except Exception as e:
                    context.update({
                        'no_record': True
                    })
                    return render(request, template_name, context)
            elif request.POST['class'] and request.POST['section']:
                context.update({
                    'error_msg': "Please Enter a Roll No.",
                    'selected_class': request.POST['class'],
                    'selected_section': request.POST['section']
                })
            elif request.POST['class'] and request.POST['roll_no']:
                context.update({
                    'error_msg': "Please Select a Section",
                    'selected_class': request.POST['class'],
                    'input_rollno': request.POST['roll_no']
                })
            elif request.POST['section'] and request.POST['roll_no']:
                context.update({
                    'error_msg': "Please Select a Class",
                    'selected_section': request.POST['section'],
                    'input_rollno': request.POST['roll_no']
                })
            else:
                context.update({
                    'error_msg': "Invalid Request"
                })

        return render(request, template_name, context)



from django.shortcuts import render
from django.http import HttpResponse
from profiles.models import class_choices, section_choices, stream_choices

# Importing models
from profiles.models import Subject, Student
from exams.models import Exam, ExamCoScholastic

# Importing Libraries
import json

# Importing Utitlities
from misc.utilities import academic_year, year_choices

# Create your views here.
def reportView(request):
    # template_name = 'exams/report.html'
    template_name = 'exams/report-2.html'

    context = {
        'class': class_choices,
        'selected_class': None,
        'selected_subject': None,
        'year': year_choices,
        'section': list(section_choices)[1:],
        'stream': list(stream_choices)[1:]
    }
    if request.method=="POST":
        if not request.POST['class']:
            context.update({
                'error_msg': "Please Select a Class"
            })
            return render(request, template_name, context)
        else:
            context.update({
                'selected_class': request.POST['class']
            })

        if not request.POST['section']:
            context.update({
                'error_msg': "Please Select a Section"
            })
            return render(request, template_name, context)
        else:
            context.update({
                'selected_section': request.POST['section']
            })
        if not request.POST['year']:
            context.update({
                'error_msg': "Please Select academic year"
            })
            return render(request, template_name, context)
        else:
            context.update({
                'selected_year': request.POST['year']
            })
        if not request.POST['subject']:
            context.update({
                'error_msg': "Please Select a Subject"
            })
            return render(request, template_name, context)
        else:
            context.update({
                'selected_subject': request.POST['subject']
            })
        
        if request.POST['class'] == '11' or request.POST['class'] == '12':
            stream = True
            if not request.POST['stream']:
                context.update({
                    'error_msg': "Please Select a stream"
                })
                return render(request, template_name, context)
            else:
                context.update({
                    'selected_stream': request.POST['stream']
                })
        else:
            stream = False
        # New Strategy
        subject = Subject.objects.get(subject_name=request.POST['subject'],subject_class=request.POST['class'],subject_board=request.user.school.school_board)
        students = request.user.school.student_set.filter(stud_class=request.POST['class'], stud_section=request.POST['section'], stud_stream=request.POST['stream'] if stream else 'NA')
        if subject.subject_type != "Co -Scholastic":
            exams = Exam.objects.filter(student__stud_school=request.user.school, exam_class=request.POST['class'], subject=subject, exam_section=request.POST['section'], exam_stream=request.POST['stream'] if stream else 'NA', exam_year=request.POST['year'])
            if (not exams) and academic_year() == request.POST['year']:
                exams = []
                for stud in students:
                    e = Exam(exam_class=stud.stud_class, student=stud, subject=subject, exam_section=stud.stud_section, exam_stream=stud.stud_stream, exam_year=request.POST['year'], exam_rollno=stud.stud_rollno)
                    e.save()
                    exams.append(e)
        else:
            context.update({
                'has_co_scholastic_subject': True
            })
            exams = ExamCoScholastic.objects.filter(exam_cs_student__stud_school=request.user.school,exam_cs_class=request.POST['class'], exam_cs_subject=subject, exam_cs_section=request.POST['section'], exam_cs_stream=request.POST['stream'] if stream else 'NA', exam_cs_year=request.POST['year'])
            if (not exams) and academic_year() == request.POST['year']:
                exams = []
                for stud in students:
                    e = ExamCoScholastic(exam_cs_student=stud, exam_cs_class=stud.stud_class, exam_cs_subject=subject, exam_cs_section=stud.stud_section, exam_cs_stream=stud.stud_stream, exam_cs_year=request.POST['year'], exam_cs_rollno=stud.stud_rollno)
                    e.save()
                    exams.append(e)
        if not exams:
            context.update({'no_record': True})
        context.update({
            'selected_class': request.POST['class'],
            'selected_subject': request.POST['subject'],
            'selected_stream': request.POST['stream'],
            'selected_section': request.POST['section'],
            'selected_year': request.POST['year'],
            'exams': exams
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
    year = academic_year()
    context = {
        'academic_year': year,
        'year': year_choices,
        'school_name': request.user.student.stud_school.school_name
    }
    if request.method=="POST":
        if not request.POST['year']:
            context.update({
                'error_msg': "Please Select Academic Year"
            })
            return [template_name, context]
        try:
            current_student = request.user.student
            scholastic_subjects = current_student.exam_set.filter(exam_year=request.POST['year'])
            co_scholastic_subjects = current_student.examcoscholastic_set.filter(exam_cs_year=request.POST['year'])
            if not (scholastic_subjects or co_scholastic_subjects):
                context.update({
                    'no_record': True
                })
            else:
                context.update({
                    'subjects': scholastic_subjects,
                    'co_subjects': co_scholastic_subjects,
                    'student': current_student,
                    'selected_year': request.POST['year'],
                    'display_class_section': scholastic_subjects and (scholastic_subjects[0].exam_class + ' - ' + scholastic_subjects[0].exam_section) or
                                                co_scholastic_subjects and (co_scholastic_subjects[0].exam_cs_class + ' - ' + co_scholastic_subjects[0].exam_cs_section),
                    'display_rollno': (scholastic_subjects and scholastic_subjects[0].exam_rollno) or (co_scholastic_subjects and co_scholastic_subjects[0].exam_cs_rollno )
                })
        except Exception as e:
            print(e)
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
            'year': year_choices,
            'stream': list(stream_choices)[2:],
            'school_name': request.user.school.school_name
        }

        if request.method=="POST":
            if not request.POST['class']:
                context.update({
                    'error_msg': "Please Select a Class"
                })
                return render(request, template_name, context)
            else:
                context.update({
                    'selected_class': request.POST['class']
                })

            if not request.POST['section']:
                context.update({
                    'error_msg': "Please Select a Section"
                })
                return render(request, template_name, context)
            else:
                context.update({
                    'selected_section': request.POST['section']
                })
            if not request.POST['year']:
                context.update({
                    'error_msg': "Please Select academic year"
                })
                return render(request, template_name, context)
            else:
                context.update({
                    'selected_year': request.POST['year']
                })
            if not request.POST['roll_no']:
                context.update({
                    'error_msg': "Please Enter a Roll No."
                })
                return render(request, template_name, context)
            else:
                context.update({
                'input_rollno': request.POST['roll_no']
                })
            if request.POST['class'] == '11' or request.POST['class'] == '12':
                stream = True
                if not request.POST['stream']:
                    context.update({
                        'error_msg': "Please Select a stream"
                    })
                    return render(request, template_name, context)
                else:
                    context.update({
                        'selected_stream': request.POST['stream']
                    })
            try:
                if stream:
                    exam = Exam.objects.filter(student__stud_school=request.user.school, exam_class=request.POST['class'], exam_section=request.POST['section'], exam_stream=request.POST['stream'], exam_rollno=request.POST['roll_no'], exam_year=request.POST['year'])
                    exam_cs = ExamCoScholastic.objects.filter(exam_cs_student__stud_school=request.user.school, exam_cs_class=request.POST['class'], exam_cs_section=request.POST['section'], exam_cs_stream=request.POST['stream'], exam_cs_year=request.POST['year'], exam_cs_rollno=request.POST['roll_no'])
                else:
                    exam = Exam.objects.filter(student__stud_school=request.user.school, exam_class=request.POST['class'], exam_section=request.POST['section'], exam_rollno=request.POST['roll_no'], exam_year=request.POST['year'], exam_school=request.user.school)
                    exam_cs = ExamCoScholastic.objects.filter(exam_cs_student__stud_school=request.user.school, exam_cs_class=request.POST['class'], exam_cs_section=request.POST['section'], exam_cs_year=request.POST['year'], exam_cs_rollno=request.POST['roll_no'], exam_cs_school=request.user.school)
                
                current_student = (exam and exam[0].student) or (exam_cs and exam_cs[0].exam_cs_student)
                scholastic_subjects = exam
                co_scholastic_subjects = exam_cs
                if not (scholastic_subjects or co_scholastic_subjects):
                    context.update({
                        'no_record': True
                    })
                else:
                    context.update({
                        'subjects': scholastic_subjects,
                        'co_subjects': co_scholastic_subjects,
                        'student': current_student,
                        'display_class_section': request.POST['class'] + " - " + request.POST['section'],
                        'display_rollno': request.POST['roll_no']
                    })
            except Exception as e:
                context.update({
                    'no_record': True
                })
                return render(request, template_name, context)
        return render(request, template_name, context)


def studentReportViewByID(request, stud_id):
    template_name = 'exams/report-by-id.html'
    year = academic_year()
    context = {
        'academic_year': year,
        'year': year_choices,
        'school_name': (request.user.is_student and request.user.student.stud_school.school_name) or request.user.school.school_name
    }
    if request.method=="POST":
        if request.POST['year']: year = request.POST['year']
        try:
            current_student = Student.objects.get(id=stud_id)
            scholastic_subjects = current_student.exam_set.filter(exam_year=year)
            co_scholastic_subjects = current_student.examcoscholastic_set.filter(exam_cs_year=year)
            if not (scholastic_subjects or co_scholastic_subjects):
                context.update({
                    'no_record': True
                })
            else:
                context.update({
                    'subjects': scholastic_subjects,
                    'co_subjects': co_scholastic_subjects,
                    'student': current_student,
                    'selected_year': request.POST['year'],
                    'display_class_section': scholastic_subjects and (scholastic_subjects[0].exam_class + ' - ' + scholastic_subjects[0].exam_section) or
                                                co_scholastic_subjects and (co_scholastic_subjects[0].exam_cs_class + ' - ' + co_scholastic_subjects[0].exam_cs_section),
                    'display_rollno': (scholastic_subjects and scholastic_subjects[0].exam_rollno) or (co_scholastic_subjects and co_scholastic_subjects[0].exam_cs_rollno )
                })
            
        except Exception as e:
            print(e)
            context.update({
                'no_record': True
            })
            return render(request, template_name, context)
    return render(request, template_name, context)
from django.http import HttpResponse
from django.views.generic import TemplateView, FormView , DetailView
from django.shortcuts import render
from django.contrib import messages
from .models import *
from .models2 import *
from .forms import *
from django.urls import reverse_lazy
from django.forms.models import model_to_dict
from misc.utilities import academic_year, year_choices
import json

def SchoolRTEDetailView(request,ac_year):
    template_name = 'schoolinfo/school_rte_details.html'
    
    choices=(
        ('I. In Private unaided and Specified Category schools under section 12(1)(c)','I. In Private unaided and Specified Category schools under section 12(1)(c) '),
        ('II. In Schools that have received land, building, equipment or other facilities at concessional rate','II. In Schools that have received land, building, equipment or other facilities at concessional rate')
    )
    response={}
    
    context = {
        'academic_year':ac_year,
        'class': choices,
        'selected_year': None
    }

    for choice in choices:
        if not SchoolRTE.objects.filter(class_name=choice[0], academic_year=ac_year, srte_school = request.user.school):
                SchoolRTE.objects.create(class_name=choice[0], academic_year=ac_year,
                    srte_school = request.user.school
                )
        response.update({
            choice[0]: SchoolRTE.objects.get(class_name=choice[0], academic_year=ac_year, srte_school = request.user.school)
        })
        context.update({
            'rows': response,
            'selected_year': ac_year
        })    
    return render(request, template_name, context)


def SchoolEWSDetailView(request,ac_year):
    template_name = 'schoolinfo/school_ews_details.html'
    
    choice='In Schools that have received land, building, equipment or other facilities at concessional rate'
    response={}
    context = {
        'academic_year':ac_year,
        'class': choice,
        'selected_year': None
    }
    if not SchoolEWS.objects.filter(class_name=choice, academic_year=ac_year, sews_school = request.user.school):
        SchoolEWS.objects.create(class_name=choice, academic_year=ac_year,sews_school = request.user.school)
    response.update({
        choice: SchoolEWS.objects.get(class_name=choice, academic_year=ac_year, sews_school = request.user.school)
    })
    context.update({
        'rows': response,
        'selected_year': ac_year
    })    
    return render(request, template_name, context)


def SchoolAnnualDetailView(request,ac_year):
    template_name = 'schoolinfo/annual_details.html'
    
    
    choices=(('Number of Students Appeared','Number of Students Appeared'),
    ('Number of Students Passed/Qualified','Number of Students Passed/Qualified'),
    ('Number of Students Passed with Marks>=60%','Number of Students Passed with Marks>=60%'))
    
    response={}
    
    context = {
        'class': choices,
    }
    for choice in choices:
        if not SchoolAnnual.objects.filter(class_name=choice[0], sa_school_name = request.user.school):
            SchoolAnnual.objects.create(class_name=choice[0],
                    sa_school_name = request.user.school
                )
        response.update({
            choice[0]: SchoolAnnual.objects.get(class_name=choice[0],sa_school_name = request.user.school)
        })
        context.update({
            'rows': response,
        })    
    return render(request, template_name, context)

def SchoolAnnualView(request):
    template_name = 'schoolinfo/school_annual.html'

    choices=(('Number of Students Appeared','Number of Students Appeared'),
    ('Number of Students Passed/Qualified','Number of Students Passed/Qualified'),
    ('Number of Students Passed with Marks>=60%','Number of Students Passed with Marks>=60%'))
    
    response={}
    
    context = {
        'class': choices,
    }
    for choice in choices:
        if not SchoolAnnual.objects.filter(class_name=choice[0], sa_school_name = request.user.school):
            SchoolAnnual.objects.create(class_name=choice[0],
                    sa_school_name = request.user.school
                )
        response.update({
            choice[0]: SchoolAnnual.objects.get(class_name=choice[0],sa_school_name = request.user.school)
        })
        context.update({
            'rows': response,
        })    
    return render(request, template_name, context)

def SaveSchoolAnnualView(request):
    data = json.loads(request.body)
    rows = data['table']

    for row in rows:
        try:
            class_val = SchoolAnnual.objects.get(sa_school_name=request.user.school,class_name=row['class_name'])
            class_val.sa_boys_gen = row['boys_1'] or None
            class_val.sa_girls_gen = row['girls_1'] or None
            class_val.sa_boys_sc = row['boys_2'] or None
            class_val.sa_girls_sc = row['girls_2'] or None
            class_val.sa_boys_st = row['boys_3'] or None
            class_val.sa_girls_st = row['girls_3'] or None
            class_val.sa_boys_obc = row['boys_4'] or None
            class_val.sa_girls_obc = row['girls_4'] or None
            class_val.sa_boys_total = row['boys_5'] or None
            class_val.sa_girls_total= row['girls_5'] or None

            # Validating and Saving the new Instance
            class_val.full_clean()
            # class_val.srte_school = request.user.school
            class_val.save()
        except Exception as e:
            print(e)
            return HttpResponse(json.dumps({ "err": str(e) }), content_type="application/json")
    messages.success(request, 'Saved successfully')
    return HttpResponse(json.dumps({ "msg": "success" }), content_type="application/json")




def SchoolIncentivesDetailView(request,ac_year):
    template_name = 'schoolinfo/incentive_details.html'
    choices=(('Free textbooks','Free textbooks'),
        ('Uniforms','Uniforms'),('Transport facility','Transport facility'),
        ('Escort','Escort'),
        ('Bicycle','Bicycle'))
    
    response={}
    
    context = {
        'class': choices,
    }
    for choice in choices:
        if not SchoolIncentives.objects.filter(class_name=choice[0], si_school_name = request.user.school):
            SchoolIncentives.objects.create(class_name=choice[0],
                    si_school_name = request.user.school
                )
        response.update({
            choice[0]: SchoolIncentives.objects.get(class_name=choice[0],si_school_name = request.user.school)
        })
        context.update({
            'rows': response,
        })    
    return render(request, template_name, context)

def SchoolIncentivesView(request):
    template_name = 'schoolinfo/school_incentives.html'

    choices=(('Free textbooks','Free textbooks'),
        ('Uniforms','Uniforms'),('Transport facility','Transport facility'),
        ('Escort','Escort'),
        ('Bicycle','Bicycle'))
    
    response={}
    
    context = {
        'class': choices,
    }
    for choice in choices:
        if not SchoolIncentives.objects.filter(class_name=choice[0], si_school_name = request.user.school):
            SchoolIncentives.objects.create(class_name=choice[0],
                    si_school_name = request.user.school
                )
        response.update({
            choice[0]: SchoolIncentives.objects.get(class_name=choice[0],si_school_name = request.user.school)
        })
        context.update({
            'rows': response,
        })    
    return render(request, template_name, context)

def SaveSchoolIncentivesView(request):
    data = json.loads(request.body)
    rows = data['table']

    for row in rows:
        try:
            class_val = SchoolIncentives.objects.get(si_school_name=request.user.school,class_name=row['class_name'])
            class_val.si_boys_gen = row['boys_1'] or None
            class_val.si_girls_gen = row['girls_1'] or None
            class_val.si_boys_sc = row['boys_2'] or None
            class_val.si_girls_sc = row['girls_2'] or None
            class_val.si_boys_st = row['boys_3'] or None
            class_val.si_girls_st = row['girls_3'] or None
            class_val.si_boys_obc = row['boys_4'] or None
            class_val.si_girls_obc = row['girls_4'] or None
            class_val.si_boys_total = row['boys_5'] or None
            class_val.si_girls_total= row['girls_5'] or None
            class_val.si_boys_muslim = row['boys_6'] or None
            class_val.si_girls_muslim = row['girls_6'] or None
            class_val.si_boys_other = row['boys_7'] or None
            class_val.si_girls_other = row['girls_7'] or None
            # Validating and Saving the new Instance
            class_val.full_clean()
            # class_val.srte_school = request.user.school
            class_val.save()
        except Exception as e:
            print(e)
            return HttpResponse(json.dumps({ "err": str(e) }), content_type="application/json")
    messages.success(request, 'Saved successfully')
    return HttpResponse(json.dumps({ "msg": "success" }), content_type="application/json")

def SchoolRTEView(request,ac_year):
    template_name = 'schoolinfo/school_rte.html'
    
    choices=(
        ('I. In Private unaided and Specified Category schools under section 12(1)(c)','I. In Private unaided and Specified Category schools under section 12(1)(c) '),
        ('II. In Schools that have received land, building, equipment or other facilities at concessional rate','II. In Schools that have received land, building, equipment or other facilities at concessional rate')
    )
    response={}
    
    context = {
        'academic_year':ac_year,
        'class': choices,
        'selected_year': None
    }

    for choice in choices:
        if not SchoolRTE.objects.filter(class_name=choice[0], academic_year=ac_year, srte_school = request.user.school):
                SchoolRTE.objects.create(class_name=choice[0], academic_year=ac_year,
                    srte_school = request.user.school
                )
        response.update({
            choice[0]: SchoolRTE.objects.get(class_name=choice[0], academic_year=ac_year, srte_school = request.user.school)
        })
        context.update({
            'rows': response,
            'selected_year': ac_year
        })    
    return render(request, template_name, context)

def SaveSchoolRTEView(request,ac_year):
    data = json.loads(request.body)
    rows = data['table']
    # print(data)
    
    # print(academic_year)
    for row in rows:
        try:
            class_val = SchoolRTE.objects.get(srte_school=request.user.school,academic_year=ac_year,class_name=row['class_name'])
            class_val.srte_class_pre_B = row['boys_pre'] or None
            class_val.srte_class_pre_G = row['girls_pre'] or None
            class_val.srte_class_I_B = row['boys_1'] or None
            class_val.srte_class_I_G = row['girls_1'] or None
            class_val.srte_class_II_B = row['boys_2'] or None
            class_val.srte_class_II_G = row['girls_2'] or None
            class_val.srte_class_III_B = row['boys_3'] or None
            class_val.srte_class_III_G = row['girls_3'] or None
            class_val.srte_class_IV_B = row['boys_4'] or None
            class_val.srte_class_IV_G = row['girls_4'] or None
            class_val.srte_class_V_B = row['boys_5'] or None
            class_val.srte_class_V_G = row['girls_5'] or None
            class_val.srte_class_VI_B = row['boys_6'] or None
            class_val.srte_class_VI_G = row['girls_6'] or None
            class_val.srte_class_VII_B = row['boys_7'] or None
            class_val.srte_class_VII_G = row['girls_7'] or None
            class_val.srte_class_VIII_B = row['boys_8'] or None
            class_val.srte_class_VIII_G = row['girls_8'] or None
            # Validating and Saving the new Instance
            class_val.full_clean()
            # class_val.srte_school = request.user.school
            class_val.save()
            
        except Exception as e:
            print(e)
            return HttpResponse(json.dumps({ "err": str(e) }), content_type="application/json")
    messages.success(request, 'Saved successfully')
    return HttpResponse(json.dumps({ "msg": "success" }), content_type="application/json")



def SchoolEWSView(request,ac_year):
    template_name = 'schoolinfo/school_ews.html'
    
    choice='In Schools that have received land, building, equipment or other facilities at concessional rate'
    response={}
    print(ac_year)
    context = {
        'academic_year':ac_year,
        'class': choice,
        'selected_year': None
    }
    if not SchoolEWS.objects.filter(class_name=choice, academic_year=ac_year, sews_school = request.user.school):
        SchoolEWS.objects.create(class_name=choice, academic_year=ac_year,sews_school = request.user.school)
    response.update({
        choice: SchoolEWS.objects.get(class_name=choice, academic_year=ac_year, sews_school = request.user.school)
    })
    context.update({
        'rows': response,
        'selected_year': ac_year
    })    
    return render(request, template_name, context)


def SaveSchoolEWSView(request,ac_year):
    data = json.loads(request.body)
    rows = data['table']
    # print(data)
    
    for row in rows:
        try:
        
            class_val = SchoolEWS.objects.get(sews_school=request.user.school,academic_year=ac_year, class_name=row['class_name'])
            class_val.sews_class_IX_B = row['boys_1'] or None
            class_val.sews_class_IX_G = row['girls_1'] or None
            class_val.sews_class_X_B = row['boys_2'] or None
            class_val.sews_class_X_G = row['girls_2'] or None
            class_val.sews_class_XI_B = row['boys_3'] or None
            class_val.sews_class_XI_G = row['girls_3'] or None
            class_val.sews_class_XII_B = row['boys_4'] or None
            class_val.sews_class_XII_G = row['girls_4'] or None
            
            # Validating and Saving the new Instance
            class_val.full_clean()
            # class_val.sews_school = request.user.school
            class_val.save()
           
        except Exception as e:
            print(e)
            return HttpResponse(json.dumps({ "err": str(e) }), content_type="application/json")
    messages.success(request, 'Saved successfully')
    return HttpResponse(json.dumps({ "msg": "success" }), content_type="application/json")


def RepeatersByGradeView(request):
    template_name = 'schoolinfo/repeaters-by-grade.html'

    class_choices = (
        ('General', 'General'),
        ('SC', 'SC'),
        ('ST', 'ST'),
        ('OBC', 'OBC'),
        ('Muslim', 'Muslim'),
        ('Christian', 'Christian'),
        ('Sikh', 'Sikh'),
        ('Buddhist', 'Buddhist'),
        ('Parsi', 'Parsi'),
        ('Jain', 'Jain'),
        ('Other', 'Other')
    )   

    response = {}
    context = {
        'year_choices': year_choices,
        'class': class_choices,
        'selected_year': None
    }
    if request.method=="POST":
        if request.POST['academic_year']:
            for choice in class_choices:
                if not RepeatersByGrade.objects.filter(class_name=choice[0], academic_year=request.POST['academic_year'], rbg_school = request.user.school):
                    RepeatersByGrade.objects.create(class_name=choice[0], academic_year=request.POST['academic_year'],
                        rbg_school = request.user.school
                    )
                response.update({
                    choice[0]: RepeatersByGrade.objects.get(class_name=choice[0], academic_year=request.POST['academic_year'], rbg_school = request.user.school)
                })
            context.update({
                'rows': response,
                'selected_year': request.POST['academic_year']
            })    
    return render(request, template_name, context)


    



def SaveRepeatersByGradeView(request):
    data = json.loads(request.body)
    rows = data['table']
    academic_year = data['academic_year'][:5] + '-' + data['academic_year'][5:]
    print(rows)
    print(academic_year)
    for row in rows:
        try:
            class_val = RepeatersByGrade.objects.get(academic_year=academic_year, class_name=row['class_name'])
            class_val.class_I_B = row['boys_1'] or None
            class_val.class_I_G = row['girls_1'] or None
            class_val.class_II_B = row['boys_2'] or None
            class_val.class_II_G = row['girls_2'] or None
            class_val.class_III_B = row['boys_3'] or None
            class_val.class_III_G = row['girls_3'] or None
            class_val.class_IV_B = row['boys_4'] or None
            class_val.class_IV_G = row['girls_4'] or None
            class_val.class_V_B = row['boys_5'] or None
            class_val.class_V_G = row['girls_5'] or None
            class_val.class_VI_B = row['boys_6'] or None
            class_val.class_VI_G = row['girls_6'] or None
            class_val.class_VII_B = row['boys_7'] or None
            class_val.class_VII_G = row['girls_7'] or None
            class_val.class_VIII_B = row['boys_8'] or None
            class_val.class_VIII_G = row['girls_8'] or None
            class_val.class_IX_B = row['boys_9'] or None
            class_val.class_IX_G = row['girls_9'] or None
            class_val.class_X_B = row['boys_10'] or None
            class_val.class_X_G = row['girls_10'] or None
            class_val.class_XI_B = row['boys_11'] or None
            class_val.class_XI_G = row['girls_11'] or None
            class_val.class_XII_B = row['boys_12'] or None
            class_val.class_XII_G = row['girls_12'] or None
            # Validating and Saving the new Instance
            class_val.full_clean()
            class_val.rbg_school = request.user.school
            class_val.save()
        except Exception as e:
            print(e)
            return HttpResponse(json.dumps({ "err": str(e) }), content_type="application/json")

    return HttpResponse(json.dumps({ "msg": "success" }), content_type="application/json")
    
class PhysicalFacilitiesView(FormView):
    model = PhysicalFacilities
    form_class = PhysicalFacilitiesForm
    template_name = 'schoolinfo/physical_facilities.html'
    # success_url = reverse_lazy('schoolinfo:physical_facilities')

    def get_object(self):
        """Check if data already exists"""
        try:
            obj = PhysicalFacilities.objects.get(pf_school = self.request.user.school, academic_year = self.kwargs['ac_year'])
            # obj = PhysicalFacilities.objects.get(pf_school = self.request.user.school)
            return obj
        except:
            return None 

    def get_initial(self):
        """Pre-fill the form if data exists"""
        obj = self.get_object()
        if obj is not None:
            return model_to_dict(obj)
        else:
            return super().get_initial()

    def get_context_data(self, **kwargs):
        """Insert the numbering into the context"""
        kwargs['numbering'] = [2.0,2.1,33,' ',' ',' ',' ',' ',2.2,2.3,' ',' ',' ',1.1,' ',' ',' ',' ',' ',' ',2.4,2.5,2.6,1.2,' ',' ',' ',2.7,2.8,2.9,2.11,2.12,1.3,' ',
        2.13,2.14,2.15,2.16,2.17,1.4,' ',2.18,1.5,' ',' ',' ',2.19,1.6,' ',2.21,2.22,2.23,' ',' ',' ',2.24,
        2.25,' ',' ',' ',' ',2.26,1.7,' ',' ',' ',' ',2.27,' ',1.8,' ',' ',' ',' ',' ',' ',' ',' ',' ',2.29,' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ']
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        input_year = self.kwargs['ac_year']
        # print(input_year)
        return reverse_lazy('schoolinfo:sections_home', kwargs={'ac_year':input_year})


    def form_valid(self, form):
        """Save to the database. If data exists, update else create new record"""
        self.object = form.save(commit=False)
        self.object.pf_school = self.request.user.school
        self.object.academic_year = self.kwargs['ac_year']
        if self.get_object() is not None:       # Assign current record primary key(id) to update existing record.
            self.object.pk = self.get_object().pk
        self.object.save()
        messages.success(self.request, 'Saved successfully')
        return super().form_valid(form)

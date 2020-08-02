from django.http import HttpResponse
from django.views.generic import TemplateView, FormView
from django.shortcuts import render
from .models import SchoolProfile, RepeatersByGrade,PhysicalFacilities
from .forms import SchoolProfileForm,PhysicalFacilitiesForm
from django.urls import reverse_lazy
from django.forms.models import model_to_dict
from misc.utilities import academic_year, year_choices
from django.contrib import messages

# Importing Libraries
import json

# Importing Libraries
import json

class SectionsHome(TemplateView):
    template_name = 'schoolinfo/sections_home.html'

class SchoolProfileView(FormView):
    model = SchoolProfile
    form_class = SchoolProfileForm
    template_name = 'schoolinfo/school_profile.html'
    success_url = reverse_lazy('schoolinfo:school_profile')

    def get_object(self):
        """Check if data already exists"""
        try:
            # obj = SchoolProfile.objects.get(sp_school = self.request.user.school, academic_year = academic_year())
            obj = SchoolProfile.objects.get(sp_school = self.request.user.school)
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
        kwargs['numbering'] = [1.1, 1.2, 1.3, 1.4,1.5,1.6,1.7,1.8,1.9,1.10,1.11,1.12,1.13,1.14,' ',' ',' ',' ',1.15,1.16,' ',' ',1.17,1.19,1.20,1.21,' ',' ',' ',' ',
        1.22,' ',' ',' ',1.23,1.24,1.25,' ',1.26,' ',1.27,1.30,1.31,1.32,' ',' ',' ',' ',' ',' ',
        1.33,' ',' ',' ',' ',1.34,1.35,1.36,' ',' ',' ',' ',1.37,' ',' ',' ',' ',' ',1.38,' ',' ',' ',' ',' ',1.39,' ',' ',' ',' ',' ',
        1.41,' ',' ',' ',' ',9999,' ',' ',1.42,' ',' ',1.43,99999,' ',' ',' ',' ',' ',' ',1.44,1.45,1.46,' ',1.47,1.49,' ',' ',' ',' ',1.51,
        999999,' ',' ',' ',' ',' ',' ',' ',' ',999999,' ',' ',' ',' ',' ',1.52,88888,' ',999999,' ',' ',' ',999999,' ',' ',' ',' ',' ',
        ' ',' ',' ',999999,' ']
        return super().get_context_data(**kwargs)


    def form_valid(self, form):
        """Save to the database. If data exists, update else create new record"""
        self.object = form.save(commit=False)
        self.object.sp_school = self.request.user.school
        self.object.academic_year = academic_year()
        if self.get_object() is not None:       # Assign current record primary key(id) to update existing record.
            self.object.pk = self.get_object().pk
        self.object.save()
        messages.add_message(self.request, messages.SUCCESS, 'Saved Successfully')
        return super().form_valid(form)

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
            class_val.save()
        except Exception as e:
            print(e)
            return HttpResponse(json.dumps({ "err": str(e) }), content_type="application/json")

    return HttpResponse(json.dumps({ "msg": "success" }), content_type="application/json")
    
class PhysicalFacilitiesView(FormView):
    model = PhysicalFacilities
    form_class = PhysicalFacilitiesForm
    template_name = 'schoolinfo/physical_facilities.html'
    success_url = reverse_lazy('schoolinfo:sections_home')

    def get_object(self):
        """Check if data already exists"""
        try:
            obj = PhysicalFacilities.objects.get(pf_school = self.request.user.school, academic_year = academic_year())
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
        kwargs['numbering'] = [2.1,2.3,2.4,' ',' ',' ',1.1,' ',' ',' ',' ',' ',' ',2.5,2.6,2.7,1.2,' ',' ',' ',2.8,2.81,2.82,2.9,2.10,1.3,' ',
        2.11,2.111,2.12,2.122,2.13,1.4,' ',2.14,1.5,' ',' ',' ',2.15,1.6,' ',2.16,2.17,2.18,' ',' ',' ',2.19,2.20,' ',' ',' ',' ',' ',' ',' ',' ',' ',
        2.21,' ',' ',' ',' ',2.31,1.7,' ',' ',' ',' ',2.33,' ']
        return super().get_context_data(**kwargs)


    def form_valid(self, form):
        """Save to the database. If data exists, update else create new record"""
        self.object = form.save(commit=False)
        self.object.pf_school = self.request.user.school
        self.object.academic_year = academic_year()
        if self.get_object() is not None:       # Assign current record primary key(id) to update existing record.
            self.object.pk = self.get_object().pk
        self.object.save()
        return super().form_valid(form)

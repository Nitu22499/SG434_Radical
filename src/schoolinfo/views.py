from django.http import HttpResponse, Http404
from django.views.generic import TemplateView, FormView , DetailView
from django.shortcuts import render
from django.contrib import messages
from .models import *
from .models2 import *
from .forms import *
from django.urls import reverse_lazy
from django.forms.models import model_to_dict
from misc.utilities import academic_year, year_choices

# Importing Libraries
import json


class Error404Mixin(DetailView):
    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            # return custom template
            return render(request, 'schoolinfo/404.html', status=404)
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

class SectionsHome(FormView):
    template_name = 'schoolinfo/sections_home.html'
    form_class = SectionHomeForm
    
    def get_context_data(self, **kwargs):
        kwargs['academic_year'] = self.kwargs['ac_year']
        kwargs['school_name'] = self.request.user.school.school_name
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        input_year = self.request.POST['academic_year_field']
        # print(input_year)
        return reverse_lazy('schoolinfo:sections_home', kwargs={'ac_year':input_year})

class ProfileDetailView(Error404Mixin):
    model=SchoolProfile
    template_name= 'schoolinfo/profile_details.html'    

class GovernmentDetailView(Error404Mixin):
    model=SchoolProfile
    template_name='schoolinfo/government_details.html'

class SchoolToiletDetailView(Error404Mixin):
    model=SchoolToilet
    template_name='schoolinfo/toilet_details.html'

class PhysicalDetailView(Error404Mixin):
    model=PhysicalFacilities
    template_name='schoolinfo/physical_details.html'

class SchoolLibraryDetailView(Error404Mixin):
    model=SchoolLibrary
    template_name='schoolinfo/library_details.html'

class SchoolItemsDetailView(Error404Mixin):
    model=SchoolItems
    template_name='schoolinfo/items_details.html'

class SchoolSafetyDetailView(Error404Mixin):
    model=SchoolSafety
    template_name='schoolinfo/safety_details.html' 

class SchoolReceiptDetailView(Error404Mixin):
    model=SchoolReceipt
    template_name='schoolinfo/receipt_details.html'


class SchoolProfileView(FormView):
    model = SchoolProfile
    form_class = SchoolProfileForm
    template_name = 'schoolinfo/school_profile.html'
    # success_url = reverse_lazy('schoolinfo:school_profile')

    def get_object(self):
        """Check if data already exists"""
        try:
            obj = SchoolProfile.objects.get(sp_school = self.request.user.school, academic_year = self.kwargs['ac_year'])
            # obj = SchoolProfile.objects.get(sp_school = self.request.user.school)
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
        kwargs['numbering'] = [1.1, 1.2, 1.3, 1.4,1.5,1.6,1.7,1.8,1.9,1.10,1.11,1.12,1.13,1.14,' ',' ',' ',' ',1.15,1.16,' ',' ',1.17,1.18,
        ' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',1.19,1.20,1.21,' ',' ',' ',' ',
        1.22,' ',' ',' ',1.23,1.24,1.25,' ',1.26,' ',1.27,1.28,' ',' ',' ',' ',1.29,' ',' ',' ',1.30,1.31,1.32,' ',' ',' ',' ',' ',' ',
        1.33,' ',' ',' ',' ',1.34,1.35,1.36,' ',' ',' ',' ',1.37,' ',' ',' ',' ',' ',1.38,' ',' ',' ',' ',' ',1.39,' ',' ',' ',' ',' ',
        1.41,' ',' ',' ',' ',9999,' ',' ',1.42,' ',' ',1.43,99999,' ',' ',' ',' ',' ',' ',1.44,1.45,1.46,' ',1.47,1.49,' ',' ',' ',' ',1.51,
        999999,' ',' ',' ',' ',' ',' ',' ',' ',999999,' ',' ',' ',' ',' ',1.52,88888,' ',999999,' ',' ',' ',999999,' ',' ',' ',' ',' ',
        ' ',' ',' ',999999,' ',2.28,' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ']
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        input_year = self.kwargs['ac_year']
        # print(input_year)
        return reverse_lazy('schoolinfo:sections_home', kwargs={'ac_year':input_year})

    def form_valid(self, form):
        """Save to the database. If data exists, update else create new record"""
        self.object = form.save(commit=False)
        self.object.sp_school = self.request.user.school
        self.object.academic_year = self.kwargs['ac_year']
        if self.get_object() is not None:       # Assign current record primary key(id) to update existing record.
            self.object.pk = self.get_object().pk
        self.object.save()
        messages.success(self.request, 'Saved successfully')
        return super().form_valid(form)



class SchoolReceiptView(FormView):
    model = SchoolReceipt
    form_class = SchoolReceiptForm
    template_name = 'schoolinfo/school_receipt.html'
    # success_url = reverse_lazy('schoolinfo:school_profile')

    def get_object(self):
        """Check if data already exists"""
        try:
            obj = SchoolReceipt.objects.get(sre_school_name = self.request.user.block.school, academic_year = self.kwargs['ac_year'])
            # obj = SchoolProfile.objects.get(sp_school = self.request.user.school)
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
        kwargs['numbering'] = []
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        input_year = self.kwargs['ac_year']
        # print(input_year)
        return reverse_lazy('schoolinfo:sections_home', kwargs={'ac_year':input_year})

    def form_valid(self, form):
        """Save to the database. If data exists, update else create new record"""
        self.object = form.save(commit=False)
        self.object.sre_school_name = self.request.user.school
        self.object.academic_year = self.kwargs['ac_year']
        if self.get_object() is not None:       # Assign current record primary key(id) to update existing record.
            self.object.pk = self.get_object().pk
        self.object.save()
        messages.success(self.request, 'Saved successfully')
        return super().form_valid(form)



class SchoolItemsView(FormView):
    model = SchoolItems
    form_class = SchoolItemsForm
    template_name = 'schoolinfo/school_items.html'
    success_url = reverse_lazy('schoolinfo:sections_home')


    def get_object(self):
        """Check if data already exists"""
        try:
            # obj = SchoolProfile.objects.get(sp_school = self.request.user.school, academic_year = academic_year())
            obj = SchoolItems.objects.get(sit_school_name = self.request.user.school)
            return obj
        except:
            return None 

    def get_success_url(self):
        input_year = self.kwargs['ac_year']
        # print(input_year)
        return reverse_lazy('schoolinfo:sections_home', kwargs={'ac_year':input_year})
   

    def get_initial(self):
        """Pre-fill the form if data exists"""
        obj = self.get_object()
        if obj is not None:
            return model_to_dict(obj)
        else:
            return super().get_initial()

    def get_context_data(self, **kwargs):
        """Insert the numbering into the context"""
        kwargs['numbering'] = []
        return super().get_context_data(**kwargs)


    def form_valid(self, form):
        """Save to the database. If data exists, update else create new record"""
        self.object = form.save(commit=False)
        self.object.sit_school_name = self.request.user.school
        self.object.academic_year = self.kwargs['ac_year']
        if self.get_object() is not None:       # Assign current record primary key(id) to update existing record.
            self.object.pk = self.get_object().pk
        self.object.save()
        messages.success(self.request, 'Saved successfully')
        return super().form_valid(form)


class SchoolLibraryView(FormView):
    model = SchoolLibrary
    form_class = SchoolLibraryForm
    template_name = 'schoolinfo/school_library.html'
    


    def get_object(self):
        """Check if data already exists"""
        try:
            # obj = SchoolProfile.objects.get(sp_school = self.request.user.school, academic_year = academic_year())
            obj = SchoolLibrary.objects.get(sli_school_name = self.request.user.school)
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
        kwargs['numbering'] = []
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        input_year = self.kwargs['ac_year']
        # print(input_year)
        return reverse_lazy('schoolinfo:sections_home', kwargs={'ac_year':input_year})


    def form_valid(self, form):
        """Save to the database. If data exists, update else create new record"""
        self.object = form.save(commit=False)
        self.object.sli_school_name = self.request.user.school
        self.object.academic_year = self.kwargs['ac_year']
        if self.get_object() is not None:       # Assign current record primary key(id) to update existing record.
            self.object.pk = self.get_object().pk
        self.object.save()
        messages.success(self.request, 'Saved successfully')
        return super().form_valid(form)

class SchoolToiletView(FormView):
    model = SchoolToilet
    form_class = SchoolToiletForm
    template_name = 'schoolinfo/school_toilet.html'
    


    def get_object(self):
        """Check if data already exists"""
        try:
            # obj = SchoolProfile.objects.get(sp_school = self.request.user.school, academic_year = academic_year())
            obj = SchoolToilet.objects.get(st_school_name = self.request.user.school)
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
        kwargs['numbering'] = []
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        input_year = self.kwargs['ac_year']
        # print(input_year)
        return reverse_lazy('schoolinfo:sections_home', kwargs={'ac_year':input_year})

    def form_valid(self, form):
        """Save to the database. If data exists, update else create new record"""
        self.object = form.save(commit=False)
        self.object.st_school_name = self.request.user.school
        self.object.academic_year = self.kwargs['ac_year']
        if self.get_object() is not None:       # Assign current record primary key(id) to update existing record.
            self.object.pk = self.get_object().pk
        self.object.save()
        messages.success(self.request, 'Saved successfully')
        return super().form_valid(form)

class SchoolSafetyView(FormView):
    model = SchoolSafety
    form_class = SchoolSafetyForm
    template_name = 'schoolinfo/school_safety.html'

    def get_object(self):
        """Check if data already exists"""
        try:
            # obj = SchoolProfile.objects.get(sp_school = self.request.user.school, academic_year = academic_year())
            obj = SchoolSafety.objects.get(sst_school_name = self.request.user.school)
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
        kwargs['numbering'] = [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',12,' ',' ',' ',' ',' ',' ',' ',' ',' ']
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        input_year = self.kwargs['ac_year']
        # print(input_year)
        return reverse_lazy('schoolinfo:sections_home', kwargs={'ac_year':input_year})

    def form_valid(self, form):
        """Save to the database. If data exists, update else create new record"""
        self.object = form.save(commit=False)
        self.object.sst_school_name = self.request.user.school
        self.object.academic_year = self.kwargs['ac_year']
        if self.get_object() is not None:       # Assign current record primary key(id) to update existing record.
            self.object.pk = self.get_object().pk
        self.object.save()
        messages.success(self.request, 'Saved successfully')
        return super().form_valid(form)
    


def SaveSchoolRTEView(request,ac_year):
    data = json.loads(request.body)
    rows = data['table']
    # print(data)
    academic_year = data['academic_year'][:4] + ' -' + data['academic_year'][5:]
    # print(academic_year)
    for row in rows:
        try:
            class_val = SchoolRTE.objects.get(srte_school=request.user.school,academic_year=academic_year,class_name=row['class_name'])
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
            messages.success(request, 'Saved successfully')
        except Exception as e:
            print(e)
            return HttpResponse(json.dumps({ "err": str(e) }), content_type="application/json")

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
    academic_year = data['academic_year'][:4] + ' -' + data['academic_year'][5:]
    print(academic_year)
    for row in rows:
        try:
        
            class_val = SchoolEWS.objects.get(sews_school=request.user.school,academic_year=academic_year, class_name=row['class_name'])
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
            messages.success(request, 'Saved successfully')
        except Exception as e:
            print(e)
            return HttpResponse(json.dumps({ "err": str(e) }), content_type="application/json")

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
            # obj = SchoolProfile.objects.get(sp_school = self.request.user.school, academic_year = academic_year())
            obj = SchoolSafety.objects.get(sst_school_name = self.request.user.school)
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
        kwargs['numbering'] = [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',12,' ',' ',' ',' ',' ',' ',' ',' ',' ']
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        input_year = self.kwargs['ac_year']
        # print(input_year)
        return reverse_lazy('schoolinfo:sections_home', kwargs={'ac_year':input_year})

    def form_valid(self, form):
        """Save to the database. If data exists, update else create new record"""
        self.object = form.save(commit=False)
        self.object.sst_school_name = self.request.user.school
        self.object.academic_year = self.kwargs['ac_year']
        if self.get_object() is not None:       # Assign current record primary key(id) to update existing record.
            self.object.pk = self.get_object().pk
        self.object.save()
        messages.success(self.request, 'Saved successfully')
        return super().form_valid(form)


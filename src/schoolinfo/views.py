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

# Importing Libraries
import json

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

class ProfileDetailView(DetailView):
    model=SchoolProfile
    template_name= 'schoolinfo/profile_details.html'
    

class GovernmentDetailView(DetailView):
    model=SchoolProfile
    template_name='schoolinfo/government_details.html'

class SchoolToiletDetailView(DetailView):
    model=SchoolToilet
    template_name='schoolinfo/toilet_details.html'

class PhysicalDetailView(DetailView):
    model=PhysicalFacilities
    template_name='schoolinfo/physical_details.html'

class SchoolLibraryDetailView(DetailView):
    model=SchoolLibrary
    template_name='schoolinfo/library_details.html'

class SchoolItemsDetailView(DetailView):
    model=SchoolItems
    template_name='schoolinfo/items_details.html'

class SchoolSafetyDetailView(DetailView):
    model=SchoolSafety
    template_name='schoolinfo/safety_details.html' 

class SchoolReceiptDetailView(DetailView):
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
            obj = SchoolReceipt.objects.get(sre_school_name = self.request.user.school, academic_year = self.kwargs['ac_year'])
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


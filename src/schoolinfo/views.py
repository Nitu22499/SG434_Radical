from django.views.generic import TemplateView, FormView
from .models import SchoolProfile,PhysicalFacilities
from .forms import SchoolProfileForm,PhysicalFacilitiesForm
from django.urls import reverse_lazy
from django.forms.models import model_to_dict
from misc.utilities import academic_year

class SectionsHome(TemplateView):
    template_name = 'schoolinfo/sections_home.html'

class SchoolProfileView(FormView):
    model = SchoolProfile
    form_class = SchoolProfileForm
    template_name = 'schoolinfo/school_profile.html'
    success_url = reverse_lazy('schoolinfo:sections_home')

    def get_object(self):
        """Check if data already exists"""
        try:
            obj = SchoolProfile.objects.get(sp_school = self.request.user.school, academic_year = academic_year())
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
        if self.get_object() is not None:       # Assign current record primary key(id) to update existing record.
            self.object.pk = self.get_object().pk
        else:                                   # Create new record.
            self.object.academic_year = academic_year()
        self.object.save()
        return super().form_valid(form)

class PhysicalFacilitiesView(FormView):
    model = PhysicalFacilities
    form_class = PhysicalFacilitiesForm
    template_name = 'schoolinfo/physical_facilities.html'
    success_url = reverse_lazy('schoolinfo:sections_home')

    def get_object(self):
        """Check if data already exists"""
        try:
            obj = PhysicalFacilities.objects.get(sp_school = self.request.user.school, academic_year = academic_year())
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
        if self.get_object() is not None:       # Assign current record primary key(id) to update existing record.
            self.object.pk = self.get_object().pk
        else:                                   # Create new record.
            self.object.academic_year = academic_year()
        self.object.save()
        return super().form_valid(form)
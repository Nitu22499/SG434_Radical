from django.shortcuts import render
from teach_staff.models import Teaching_Staff_Info, Teaching_Staff_NonTeachers_Info
from django.urls import reverse_lazy
# Create your views here.
from .forms import NonTeaching_Staff_Form, Teaching_Staff_Form
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView, TemplateView
from django.contrib import messages


class Teaching_Staff_NonTeachers_InfoListView(ListView):
    model = Teaching_Staff_NonTeachers_Info
    template_name = "NonTeachers_info_list.html"
    context_object_name = 'NonTeachers_list_obj'
    

class Teaching_Staff_NonTeachers_InfoDetailView(DetailView):
    model = Teaching_Staff_NonTeachers_Info
    template_name = "NonTeachers_Info_Detail.html"
    context_object_name = 'NonTeachers_detail_obj'

class Teaching_Staff_NonTeachers_InfoCreateView(CreateView):
    model = Teaching_Staff_NonTeachers_Info
    
    template_name = 'NonTeachers_Create.html'
    form_class = NonTeaching_Staff_Form

    def form_valid(self, form):
        """Save to the database. If data exists, update else create new record"""
        self.object = form.save(commit=False)
        self.object.NonTeachers_School = self.request.user.school
        
       
        self.object.save()
        messages.add_message(self.request, messages.SUCCESS, 'Saved Successfully')
        return super().form_valid(form)

class Teaching_Staff_NonTeachers_InfoUpdateView(UpdateView):
    
    model = Teaching_Staff_NonTeachers_Info
    template_name = 'NonTeachers_Create.html'
    form_class = NonTeaching_Staff_Form

class Teaching_Staff_NonTeachers_InfoDeleteView(DeleteView):
    model = Teaching_Staff_NonTeachers_Info
    success_url = reverse_lazy('teach_staff:NonTeachers_List')
    template_name = 'NonTeachers_Delete.html'
    context_object_name = 'NonTeachers_Delete_Object'




    ###########################################################333

class Teaching_Staff_TemplateView(TemplateView):
    template_name = 'teach_staff_base.html'

class Teaching_Staff_InfoListView(ListView):
    model = Teaching_Staff_Info
    template_name = "Teachers_info_list.html"
    context_object_name = 'Teaching_Staff_Info_List_Object'

class Teaching_Staff_InfoDetailView(DetailView):
    model = Teaching_Staff_Info
    template_name = "Teaching_Staff_Info_Detail.html"
    context_object_name = 'Teaching_Staff_Info_Detail_Object'


class Teaching_Staff_InfoCreateView(CreateView):
    model = Teaching_Staff_Info
    
    template_name = 'Teacher_Staff_Info_Create.html'
    form_class = Teaching_Staff_Form

    def form_valid(self, form):
        """Save to the database. If data exists, update else create new record"""
        self.object = form.save(commit=False)
        self.object.Teacher_School = self.request.user.school
        
       
        self.object.save()
        messages.add_message(self.request, messages.SUCCESS, 'Saved Successfully')
        return super().form_valid(form)

class Teaching_Staff_InfoUpdateView(UpdateView):
    
    model = Teaching_Staff_Info
    template_name = 'Teacher_Staff_Info_Create.html'
    form_class = Teaching_Staff_Form

class Teaching_Staff_InfoDeleteView(DeleteView):
    model = Teaching_Staff_Info
    success_url = reverse_lazy('teach_staff:Teacher_List')
    template_name = 'Teacher_Staff_Info_Delete.html'
    context_object_name = 'Teacher_Staff_Info_Delete_Object'



    




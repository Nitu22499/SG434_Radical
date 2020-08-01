from django.views.generic import TemplateView, FormView
from django.shortcuts import render
from .models import SchoolProfile, RepeatersByGrade
from .forms import SchoolProfileForm
from django.urls import reverse_lazy
from django.forms.models import model_to_dict
from misc.utilities import academic_year, year_choices

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
        kwargs['numbering'] = [1.1, 1.2, 1.3, '']
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
                if not RepeatersByGrade.objects.filter(class_name=choice[0], academic_year=request.POST['academic_year']):
                    RepeatersByGrade.objects.create(class_name=choice[0], academic_year=request.POST['academic_year'])
                response.update({
                    choice[0]: RepeatersByGrade.objects.get(class_name=choice[0], academic_year=request.POST['academic_year'])
                })
            context.update({
                'rows': response,
                'selected_year': request.POST['academic_year']
            })    
    return render(request, template_name, context)
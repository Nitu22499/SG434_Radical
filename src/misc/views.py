from django.views.generic import TemplateView
from profiles.models import District, Block
from django.shortcuts import render

class Home(TemplateView):
    template_name = 'base.html'

    def get_template_names(self):
        if self.request.user.is_school_admin:
            self.template_name = 'misc/school_home.html'
        elif self.request.user.is_student:
            self.template_name = 'misc/student_home.html'
        elif self.request.user.is_block_admin:
            self.template_name = 'misc/block_home.html'
        elif self.request.user.is_district_admin:
            self.template_name = 'misc/district_home.html'
        return [self.template_name]

def load_blocks(request):
    district_id = request.GET.get('district')
    blocks = Block.objects.filter(block_district_id=district_id).order_by('block_name')
    return render(request, 'misc/block_dropdown_options.html', {'blocks': blocks})  
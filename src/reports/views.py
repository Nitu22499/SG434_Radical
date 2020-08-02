from django.views.generic import TemplateView, FormView
from .forms import ReportForm


class ReportHome(TemplateView):
    template_name = 'reports/reports_home.html'

class SchoolsByMgmt(FormView):
    template_name = 'reports/reports_form.html'
    form_class = ReportForm

  
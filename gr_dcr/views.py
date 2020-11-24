from django.views.generic import TemplateView
from django.views import generic

class DCRPage(TemplateView):
    template_name = 'DCR_template.html'

class DCRTable(TemplateView):
    template_name = 'DCR_table.html'

class ThanksPage(TemplateView):
    template_name = 'thanks.html'

class HomePage(TemplateView):
    template_name = 'index.html'

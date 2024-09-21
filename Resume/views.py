from django.shortcuts import render
from Resume import models
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, View, ListView, UpdateView, DeleteView
from Resume.forms import ResumeForm , ProjectsForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

# портфолио + его главная страница
class ResumeDetailView(DetailView):
    model = models.Resume
    template_name = "resume/resume_detail.html"
    context_object_name = "resume"

class ResumeCreateView(CreateView):
    model = models.Resume
    form_class = ResumeForm
    template_name = "resume/resume_form.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        
        if not form.instance.image:
            messages.add_message(self.request, messages.WARNING, "Пожалуйста, добавьте изображение.")
            return self.form_invalid(form)  
        
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('resume:resume_main', kwargs={'pk': self.object.pk})

    
class ResumeUpdateView(UpdateView):
    model = models.Resume
    form_class = ResumeForm
    template_name ="resume/resume_form.html"    

    def get_success_url(self):
        return reverse_lazy('resume:resume_main', kwargs={'pk': self.object.pk})

class ResumeMainView(DetailView):
    model = models.Resume
    template_name = "resume/resume_main.html"
    context_object_name = "resume"

# проэкты портфолио

class ProjectsInformationView(ListView):
    model = models.ResumeProjects
    template_name = 'resume/projects_list.html'
    context_object_name = "projects"

    def get_queryset(self):
        return super().get_queryset().filter(resume=self.resume)
    
    def dispatch(self, request: HttpRequest, pk, *args: reverse_lazy, **kwargs: reverse_lazy) -> HttpResponse:
        self.resume = get_object_or_404(models.Resume, id = pk )
        return super().dispatch(request, *args, **kwargs)

class ProjectsCreateView(CreateView):
    model = models.ResumeProjects
    form_class = ProjectsForm
    template_name = "resume/projects_form.html"    

    def dispatch(self,*args, **kwargs):
        self.portfolio = get_object_or_404(models.Resume,id=self.kwargs.get('resume_id'))
        return super().dispatch(*args, **kwargs)
    
    def form_valid(self, form):
        form.instance.resume = self.resume
        return super().form_valid(form)
    
    

class ProjectsUpdateView(UpdateView):
    model = models.ResumeProjects
    form_class = ProjectsForm
    template_name = "resume/projects_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs.get('pk')
        return context
    
    def get_success_url(self):
        return reverse_lazy('resume:resume_main', kwargs={'pk': self.object.resume.pk})
    
class ProjectsDeleteView(View):
   def post(self,request,pk):
       project = get_object_or_404(models.ResumeProjects, pk=pk)
       resume = project.resume
       project.delete()
       return redirect('resume:resume_main', resume.pk)

def home(request):
    return render(request, 'Resume/home.html')



from django.template.loader import get_template
from io import BytesIO
import xhtml2pdf.pisa as pisa
from django.http import HttpResponse
from . import models

def render_to_pdf(template_src, context_dict, filename='resume_doc.pdf'):
    """ Генерация PDF файла и возвращение его в виде HTTP-ответа """
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(
        BytesIO(html.encode('utf-8')), 
        result, 
        encoding='UTF-8',
        show_error_as_pdf=True
    )
    if not pdf.err:
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    return HttpResponse('We had some errors!')

def resume_text(request, pk):
    try:
        resume = models.Resume.objects.get(pk=pk, user=request.user)
    except models.Resume.DoesNotExist:
        return HttpResponse('Resume not found', status=404)

    context = {
        'resume': resume,
    }
    return render_to_pdf('Resume/resume_detail_pdf.html', context, 'resume_doc.pdf')

class ResumeTemplateListView(ListView):
    model = models.ResumeTemplate
    template_name = 'resume/template_list.html'
    context_object_name = 'templates'

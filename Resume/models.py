from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class ResumeTemplate(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    template_file = models.FileField(upload_to='templates/')
    def __str__(self):
        return self.name
    
class Resume (models.Model):
    # 1 column
    name = models.CharField(max_length=250)
    surname = models.CharField(max_length=250)
    birth_date = models.DateField()
    birth_place = models.TextField()
    image = models.ImageField(upload_to="images/", null=True, blank=True)
    # 2 column
    residance_address = models.TextField()
    tel_num = models.IntegerField()
    email = models.EmailField(max_length=511)
    # 3 column
    studying = models.TextField()
    work_exp = models.TextField()
    knowladge = models.TextField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    template = models.ForeignKey(ResumeTemplate, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('resume:projects_create', kwargs={'resume_id': self.pk})
    
class ResumeProjects(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=511)
    description = models.TextField()
    due_date = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('resume:resume_main', kwargs={'pk': self.resume.pk})

    
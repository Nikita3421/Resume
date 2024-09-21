from django.shortcuts import render
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from Resume import models

class ResumeForm(forms.ModelForm):
    
    class Meta:
        model = models.Resume
        fields = [
            'name',
            'surname',
            'birth_date',
            'birth_place',
            'image',
            'residance_address',
            'tel_num', 
            'email', 
            'studying', 
            'work_exp',
            'knowladge',
            ]
        
    def __init__(self, *args, **kwargs):
        super(ResumeForm, self).__init__(*args, **kwargs)
        self.fields['template'].queryset = models.ResumeTemplate.objects.all()
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})
    
    
class ProjectsForm(forms.ModelForm):
    class Meta:
        model = models.ResumeProjects
        fields = [
            'title',
            'description',
            ]

    def __init__(self, *args, **kwargs):
        super(ProjectsForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})        

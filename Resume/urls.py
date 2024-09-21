from django.urls import path
# from .views import view netu
from Resume import views

urlpatterns = [
    path('', views.home, name='home'),
    path('resume_pdf/<int:pk>/', views.resume_text, name='resume_pdf'),
    path('resume_main/<int:pk>/', views.ResumeMainView.as_view(), name="resume_main"), #main page
    path('resume_create/', views.ResumeCreateView.as_view(), name='resume_create'),
    path('resume_create_pdf/', views.ResumeCreateView.as_view(), name='resume_create_pdf'),
    path('resume_detail/<int:pk>/',views.ResumeDetailView.as_view(), name="resume_detail"),#resume
    path('resume_update/<int:pk>/', views.ResumeUpdateView.as_view(), name='resume_update'),
    path('projects_list/<int:pk>/', views.ProjectsInformationView.as_view(), name="projects_list"),
    path('projects_create/<int:resume_id>', views.ProjectsCreateView.as_view(), name="projects_create"),
    path('projects_update/<int:pk>', views.ProjectsUpdateView.as_view(), name="projects_update"),
    path('projects_delete/<int:pk>', views.ProjectsDeleteView.as_view(), name="projects_delete"),
]

app_name = 'resume'
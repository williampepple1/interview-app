from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [
    path('', views.assessment_list, name='assessment_list'),
    path('assessment/<int:assessment_id>/start/', views.start_assessment, name='start_assessment'),
    path('assessment/<int:assessment_id>/question/', views.take_question, name='take_question'),
    path('assessment/<int:assessment_id>/submit/', views.submit_answer, name='submit_answer'),
    path('assessment/<int:assessment_id>/results/', views.assessment_results, name='assessment_results'),
    path('create/', views.create_assessment, name='create_assessment'),
    path('assessment/<int:assessment_id>/retake/', views.retake_assessment, name='retake_assessment'),
] 
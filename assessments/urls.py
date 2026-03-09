from django.urls import path
from . import views

app_name = 'assessments'

urlpatterns = [
    path('kelas/<int:kelas_id>/grading/', views.grading_spreadsheet, name='grading_spreadsheet'),
    path('kelas/<int:kelas_id>/report/', views.cpl_report, name='cpl_report'),
    path('kelas/<int:kelas_id>/upload-peserta/', views.upload_peserta_excel, name='upload_peserta'),
]
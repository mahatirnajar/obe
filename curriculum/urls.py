from django.urls import path
from . import views

app_name = 'curriculum'

urlpatterns = [
    path('mata-kuliah/<int:mk_id>/download-rps-pdf/', views.generate_rps_pdf, name='download_rps_pdf'),
]
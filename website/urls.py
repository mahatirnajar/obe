from django.urls import path
from . import views

app_name = 'website'

urlpatterns = [
    # Beranda
    path('', views.index, name='index'),

    # Profil
    path('sejarah/', views.sejarah, name='sejarah'),
    path('visi-misi/', views.visi_misi, name='visi_misi'),
    path('struktur-organisasi/', views.struktur_organisasi, name='struktur_organisasi'),

    # SDM
    path('dosen/', views.dosen, name='dosen'),
    path('tenaga-kependidikan/', views.tendik, name='tendik'),

    # Berita & Pengumuman
    path('berita/', views.berita_list, name='berita_list'),
    path('berita/<slug:slug>/', views.berita_detail, name='berita_detail'),

    # Fasilitas
    path('fasilitas/', views.fasilitas, name='fasilitas'),

    # Galeri
    path('galeri/', views.galeri, name='galeri'),

    # Kemahasiswaan
    path('alumni/', views.alumni, name='alumni'),

    # Kontak
    path('kontak/', views.kontak, name='kontak'),
]

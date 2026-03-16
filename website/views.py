from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from .models import (
    Berita, Dosen, TenagaKependidikan,
    Fasilitas, Galeri, Alumni, ProfilProdi, Kontak
)
from .forms import KontakForm


# ─────────────────────────────────────────
# HALAMAN UTAMA
# ─────────────────────────────────────────

def index(request):
    """Halaman beranda."""
    berita_terbaru = Berita.objects.filter(diterbitkan=True)[:6]
    galeri_terbaru = Galeri.objects.filter(ditampilkan=True)[:8]
    dosen_list = Dosen.objects.filter(aktif=True)[:6]
    alumni_list = Alumni.objects.filter(ditampilkan=True)[:4]

    try:
        profil = ProfilProdi.objects.first()
    except ProfilProdi.DoesNotExist:
        profil = None

    context = {
        'berita_terbaru': berita_terbaru,
        'galeri_terbaru': galeri_terbaru,
        'dosen_list': dosen_list,
        'alumni_list': alumni_list,
        'profil': profil,
    }
    return render(request, 'website/index.html', context)

# ─────────────────────────────────────────
# PROFIL PRODI
# ─────────────────────────────────────────

def sejarah(request):
    profil = ProfilProdi.objects.first()
    return render(request, 'website/profil/sejarah.html', {'profil': profil})


def visi_misi(request):
    profil = ProfilProdi.objects.first()
    return render(request, 'website/profil/visi_misi.html', {'profil': profil})


def struktur_organisasi(request):
    koordinator = Dosen.objects.filter(jabatan='koordinator', aktif=True).first()
    return render(request, 'website/profil/struktur_organisasi.html', {
        'koordinator': koordinator,
    })


# ─────────────────────────────────────────
# SDM
# ─────────────────────────────────────────

def dosen(request):
    dosen_list = Dosen.objects.filter(aktif=True)
    return render(request, 'website/sdm/dosen.html', {'dosen_list': dosen_list})


def tendik(request):
    tendik_list = TenagaKependidikan.objects.filter(aktif=True)
    return render(request, 'website/sdm/tendik.html', {'tendik_list': tendik_list})


# ─────────────────────────────────────────
# BERITA & PENGUMUMAN
# ─────────────────────────────────────────

def berita_list(request):
    kategori = request.GET.get('kategori', '')
    qs = Berita.objects.filter(diterbitkan=True)
    if kategori:
        qs = qs.filter(kategori=kategori)

    paginator = Paginator(qs, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'website/berita/list.html', {
        'page_obj': page_obj,
        'kategori_aktif': kategori,
        'kategori_choices': Berita.KATEGORI_CHOICES,
    })


def berita_detail(request, slug):
    berita = get_object_or_404(Berita, slug=slug, diterbitkan=True)
    berita_terkait = Berita.objects.filter(
        diterbitkan=True,
        kategori=berita.kategori
    ).exclude(pk=berita.pk)[:4]

    return render(request, 'website/berita/detail.html', {
        'berita': berita,
        'berita_terkait': berita_terkait,
    })


# ─────────────────────────────────────────
# FASILITAS
# ─────────────────────────────────────────

def fasilitas(request):
    laboratorium = Fasilitas.objects.filter(jenis='laboratorium')
    ruang_kuliah = Fasilitas.objects.filter(jenis='ruang_kuliah')
    ruang_dosen = Fasilitas.objects.filter(jenis='ruang_dosen')

    return render(request, 'website/fasilitas.html', {
        'laboratorium': laboratorium,
        'ruang_kuliah': ruang_kuliah,
        'ruang_dosen': ruang_dosen,
    })


# ─────────────────────────────────────────
# GALERI
# ─────────────────────────────────────────

def galeri(request):
    galeri_list = Galeri.objects.filter(ditampilkan=True)
    paginator = Paginator(galeri_list, 12)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'website/galeri.html', {'page_obj': page_obj})


# ─────────────────────────────────────────
# KEMAHASISWAAN
# ─────────────────────────────────────────

def alumni(request):
    angkatan = request.GET.get('angkatan', '')
    qs = Alumni.objects.filter(ditampilkan=True)
    if angkatan:
        qs = qs.filter(angkatan=angkatan)

    angkatan_list = Alumni.objects.filter(
        ditampilkan=True
    ).values_list('angkatan', flat=True).distinct().order_by('-angkatan')

    paginator = Paginator(qs, 12)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'website/kemahasiswaan/alumni.html', {
        'page_obj': page_obj,
        'angkatan_list': angkatan_list,
        'angkatan_aktif': angkatan,
    })


# ─────────────────────────────────────────
# KONTAK
# ─────────────────────────────────────────

def kontak(request):
    profil = ProfilProdi.objects.first()
    if request.method == 'POST':
        form = KontakForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Pesan Anda berhasil dikirim. Kami akan menghubungi Anda segera.'
            )
            return redirect('website:kontak')
    else:
        form = KontakForm()

    return render(request, 'website/kontak.html', {
        'form': form,
        'profil': profil,
    })

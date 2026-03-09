from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from nested_admin import NestedModelAdmin, NestedStackedInline, NestedTabularInline
from .models import Mahasiswa, Kelas, PesertaKelas, NilaiSubCPMK

@admin.register(Mahasiswa)
class MahasiswaAdmin(admin.ModelAdmin):
    list_display = ('nim', 'nama', 'angkatan')
    search_fields = ('nim', 'nama')
    list_filter = ('angkatan',)
    ordering = ('nim',)

# ==========================================
# KONFIGURASI NESTED INLINE UNTUK PENILAIAN
# ==========================================

# 1. Level Cucu: Tabel Input Nilai
class NilaiSubCPMKInline(NestedTabularInline):
    model = NilaiSubCPMK
    extra = 0 # Tidak menampilkan baris kosong secara default agar tidak penuh
    fields = ('sub_cpmk', 'nilai_angka', 'tampil_nilai_terbobot')
    readonly_fields = ('tampil_nilai_terbobot',) # Kolom ini dihitung otomatis, tidak bisa diedit manual

    def tampil_nilai_terbobot(self, obj):
        # Mengecek apakah objek sudah disimpan di database
        if obj.pk: 
            return obj.nilai_terbobot
        return "-"
    tampil_nilai_terbobot.short_description = "Poin Terbobot"

# 2. Level Anak: Data Peserta Kelas (KRS Mahasiswa)
class PesertaKelasInline(NestedStackedInline):
    model = PesertaKelas
    extra = 0
    inlines = [NilaiSubCPMKInline]
    # Autocomplete sangat penting agar browser tidak hang meload ribuan nama mahasiswa di dropdown
    autocomplete_fields = ['mahasiswa'] 


@admin.register(Kelas)
class KelasAdmin(NestedModelAdmin):
    # Mengganti 'tombol_upload_peserta' menjadi 'aksi_pintasan'
    list_display = ('mata_kuliah', 'nama_kelas', 'tahun_akademik', 'aksi_pintasan')
    list_filter = ('tahun_akademik', 'mata_kuliah')
    search_fields = ('nama_kelas', 'mata_kuliah__nama', 'mata_kuliah__kode')
    inlines = [PesertaKelasInline]
    
    # Masukkan fungsi baru ke dalam readonly_fields
    readonly_fields = ('aksi_pintasan',)

    def aksi_pintasan(self, obj):
        # Tombol hanya akan muncul jika Kelas sudah di-save (memiliki ID)
        if obj.pk:
            # Mengambil URL dari masing-masing halaman berdasarkan ID kelas
            url_upload = reverse('assessments:upload_peserta', args=[obj.pk])
            url_grading = reverse('assessments:grading_spreadsheet', args=[obj.pk])
            url_report = reverse('assessments:cpl_report', args=[obj.pk])
            
            # Merender 3 tombol berjejer dengan warna berbeda
            return format_html(
                '<div style="display: flex; flex-wrap: wrap; gap: 8px;">'
                '<a href="{}" style="background-color: #17a2b8; color: white; padding: 6px 12px; border-radius: 4px; font-weight: bold; text-decoration: none; white-space: nowrap; font-size: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.2);">📊 Upload Peserta</a>'
                '<a href="{}" style="background-color: #28a745; color: white; padding: 6px 12px; border-radius: 4px; font-weight: bold; text-decoration: none; white-space: nowrap; font-size: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.2);">📝 Matriks Nilai</a>'
                '<a href="{}" style="background-color: #ffc107; color: black; padding: 6px 12px; border-radius: 4px; font-weight: bold; text-decoration: none; white-space: nowrap; font-size: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.2);">📈 Laporan CPL</a>'
                '</div>',
                url_upload, url_grading, url_report
            )
        return "-"
    aksi_pintasan.short_description = "Pintasan Aksi"
    aksi_pintasan.allow_tags = True

# ==========================================
# (Opsional) Pendaftaran PesertaKelas Mandiri
# ==========================================
@admin.register(PesertaKelas)
class PesertaKelasAdmin(admin.ModelAdmin):
    list_display = ('mahasiswa', 'kelas')
    search_fields = ('mahasiswa__nama', 'mahasiswa__nim', 'kelas__mata_kuliah__nama')
    list_filter = ('kelas__tahun_akademik', 'kelas__mata_kuliah')


from django.contrib import admin
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

# 3. Level Induk: Data Kelas Utama
@admin.register(Kelas)
class KelasAdmin(NestedModelAdmin):
    list_display = ('mata_kuliah', 'nama_kelas', 'tahun_akademik')
    list_filter = ('tahun_akademik', 'mata_kuliah')
    search_fields = ('nama_kelas', 'mata_kuliah__nama', 'mata_kuliah__kode')
    inlines = [PesertaKelasInline]

# ==========================================
# (Opsional) Pendaftaran PesertaKelas Mandiri
# ==========================================
@admin.register(PesertaKelas)
class PesertaKelasAdmin(admin.ModelAdmin):
    list_display = ('mahasiswa', 'kelas')
    search_fields = ('mahasiswa__nama', 'mahasiswa__nim', 'kelas__mata_kuliah__nama')
    list_filter = ('kelas__tahun_akademik', 'kelas__mata_kuliah')
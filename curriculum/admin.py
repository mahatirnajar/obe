from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from nested_admin import NestedModelAdmin, NestedTabularInline, NestedStackedInline
from .models import ProfilLulusan, CPL, MataKuliah, RPS, CPMK, SubCPMK

@admin.register(ProfilLulusan)
class ProfilLulusanAdmin(admin.ModelAdmin):
    list_display = ('kode', 'nama')
    search_fields = ('kode', 'nama')

@admin.register(CPL)
class CPLAdmin(admin.ModelAdmin):
    list_display = ('kode', 'get_deskripsi_singkat')
    search_fields = ('kode', 'deskripsi')
    filter_horizontal = ('profil_lulusan',) 

    def get_deskripsi_singkat(self, obj):
        return obj.deskripsi[:75] + '...' if len(obj.deskripsi) > 75 else obj.deskripsi
    get_deskripsi_singkat.short_description = 'Deskripsi'

# ==========================================
# KONFIGURASI NESTED INLINE
# ==========================================

# 1. Level Cucu: Sub-CPMK (Bentuknya tabel ringkas)
class SubCPMKInline(NestedTabularInline):
    model = SubCPMK
    extra = 1
    fields = ('kode', 'deskripsi', 'bentuk_penilaian', 'bobot_persentase')

# 2. Level Anak: CPMK (Bentuknya blok/stacked karena ada ManyToMany CPL)
class CPMKInline(NestedStackedInline):
    model = CPMK
    extra = 1
    # filter_horizontal tidak jalan di inline bawaan, kita gunakan gaya standard
    # Masukkan inline cucu (Sub-CPMK) ke dalam anak (CPMK)
    inlines = [SubCPMKInline] 


@admin.register(RPS)
class RPSAdmin(admin.ModelAdmin):
    list_display = ('mata_kuliah', 'tanggal_penyusunan')
    search_fields = ('mata_kuliah__nama', 'mata_kuliah__kode')
    list_filter = ('tanggal_penyusunan',)



@admin.register(MataKuliah)
class MataKuliahAdmin(NestedModelAdmin):
    list_display = ('kode', 'nama', 'sks', 'semester', 'tombol_download_rps')
    # list_filter = ('semester', 'sks')
    search_fields = ('kode', 'nama')
    ordering = ('semester', 'kode')
    
    # Masukkan inline anak (CPMK) ke dalam induk (Mata Kuliah)
    inlines = [CPMKInline]

    def tombol_download_rps(self, obj):
        if obj.pk:
            # UBAH NAMA URL KE download_rps_pdf
            url = reverse('curriculum:download_rps_pdf', args=[obj.pk]) 
            return format_html(
                '<a class="button" href="{}" style="background-color: #dc3545; color: white; padding: 5px 10px; border-radius: 4px; font-weight: bold;">📄 Cetak PDF</a>', 
                url
            )
        return "-"
    tombol_download_rps.short_description = "Aksi Cetak"
    tombol_download_rps.allow_tags = True
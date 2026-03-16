from django.contrib import admin
from .models import (
    Berita, Dosen, TenagaKependidikan,
    Fasilitas, Galeri, Alumni, ProfilProdi, Kontak
)


@admin.register(Berita)
class BeritaAdmin(admin.ModelAdmin):
    list_display = ('judul', 'kategori', 'diterbitkan', 'tanggal_dibuat')
    list_filter = ('kategori', 'diterbitkan')
    list_editable = ('diterbitkan',)
    search_fields = ('judul', 'isi')
    prepopulated_fields = {'slug': ('judul',)}
    date_hierarchy = 'tanggal_dibuat'


@admin.register(Dosen)
class DosenAdmin(admin.ModelAdmin):
    list_display  = ('nama', 'jabatan', 'pendidikan_terakhir', 'bidang_keahlian', 'urutan', 'aktif')
    list_filter = ('jabatan', 'pendidikan_terakhir', 'aktif')
    list_editable = ('aktif', 'urutan')
    search_fields = ('nama', 'bidang_keahlian', 'nidn')

    fieldsets = (
        ('Informasi Dasar', {
            'fields': ('nama', 'nip', 'nidn', 'jabatan', 'pendidikan_terakhir', 'bidang_keahlian')
        }),
        ('Kontak & Media', {
            'fields': ('foto', 'email', 'google_scholar')
        }),
        ('Pengaturan', {
            'fields': ('urutan', 'aktif')
        }),
    )


@admin.register(TenagaKependidikan)
class TenagaKependidikanAdmin(admin.ModelAdmin):
    list_display = ('nama', 'jabatan', 'email', 'aktif')
    list_filter = ('aktif',)
    search_fields = ('nama', 'jabatan')


@admin.register(Fasilitas)
class FasilitasAdmin(admin.ModelAdmin):
    list_display = ('nama', 'jenis', 'urutan')
    list_filter = ('jenis',)
    list_editable = ('urutan',)


@admin.register(Galeri)
class GaleriAdmin(admin.ModelAdmin):
    list_display = ('judul', 'tanggal', 'ditampilkan')
    list_filter = ('ditampilkan',)
    list_editable = ('ditampilkan',)
    date_hierarchy = 'tanggal'


@admin.register(Alumni)
class AlumniAdmin(admin.ModelAdmin):
    list_display = ('nama', 'angkatan', 'tahun_lulus', 'pekerjaan', 'instansi', 'ditampilkan')
    list_filter = ('angkatan', 'tahun_lulus', 'ditampilkan')
    list_editable = ('ditampilkan',)
    search_fields = ('nama', 'pekerjaan', 'instansi')


@admin.register(ProfilProdi)
class ProfilProdiAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Konten Utama', {
            'fields': ('sejarah', 'visi', 'misi', 'tujuan')
        }),
        ('Statistik', {
            'fields': ('akreditasi', 'tahun_berdiri', 'jumlah_mahasiswa', 'jumlah_dosen')
        }),
        ('Kontak Prodi', {
            'fields': ('email_prodi', 'telepon', 'alamat')
        }),
    )

    def has_add_permission(self, request):
        # Hanya boleh ada satu record ProfilProdi
        return not ProfilProdi.objects.exists()


@admin.register(Kontak)
class KontakAdmin(admin.ModelAdmin):
    list_display = ('nama', 'email', 'subjek', 'tanggal', 'sudah_dibaca')
    list_filter = ('sudah_dibaca',)
    list_editable = ('sudah_dibaca',)
    readonly_fields = ('nama', 'email', 'subjek', 'pesan', 'tanggal')
    date_hierarchy = 'tanggal'

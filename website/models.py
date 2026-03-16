from django.db import models
from django.utils import timezone


class Berita(models.Model):
    KATEGORI_CHOICES = [
        ('berita', 'Berita'),
        ('pengumuman', 'Pengumuman'),
        ('kegiatan', 'Kegiatan'),
        ('prestasi', 'Prestasi'),
    ]

    judul = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    kategori = models.CharField(max_length=20, choices=KATEGORI_CHOICES, default='berita')
    isi = models.TextField()
    ringkasan = models.TextField(max_length=300, blank=True)
    gambar = models.ImageField(upload_to='berita/', blank=True, null=True)
    diterbitkan = models.BooleanField(default=False)
    tanggal_dibuat = models.DateTimeField(default=timezone.now)
    tanggal_diperbarui = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Berita'
        verbose_name_plural = 'Berita'
        ordering = ['-tanggal_dibuat']

    def __str__(self):
        return self.judul


class Dosen(models.Model):
    JABATAN_CHOICES = [
        ('koordinator', 'Koordinator Prodi'),
        ('dosen', 'Dosen'),
        ('dosen_luar', 'Dosen Luar Biasa'),
    ]

    PENDIDIKAN_CHOICES = [
        ('s3', 'S3 / Doktor'),
        ('s2', 'S2 / Magister'),
    ]

    nama = models.CharField(max_length=150)
    nip = models.CharField(max_length=30, blank=True)
    nidn = models.CharField(max_length=20, blank=True)
    jabatan = models.CharField(max_length=20, choices=JABATAN_CHOICES, default='dosen')
    pendidikan_terakhir = models.CharField(max_length=5, choices=PENDIDIKAN_CHOICES, default='s2')
    bidang_keahlian = models.CharField(max_length=200)
    foto = models.ImageField(upload_to='dosen/', blank=True, null=True)
    email = models.EmailField(blank=True)
    google_scholar = models.URLField(blank=True)
    urutan = models.PositiveIntegerField(default=0, help_text='Urutan tampil di halaman')
    aktif = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Dosen'
        verbose_name_plural = 'Dosen'
        ordering = ['urutan', 'nama']

    def __str__(self):
        return self.nama


class TenagaKependidikan(models.Model):
    nama = models.CharField(max_length=150)
    nip = models.CharField(max_length=30, blank=True)
    jabatan = models.CharField(max_length=150)
    foto = models.ImageField(upload_to='tendik/', blank=True, null=True)
    email = models.EmailField(blank=True)
    aktif = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Tenaga Kependidikan'
        verbose_name_plural = 'Tenaga Kependidikan'
        ordering = ['nama']

    def __str__(self):
        return self.nama


class Fasilitas(models.Model):
    JENIS_CHOICES = [
        ('laboratorium', 'Laboratorium'),
        ('ruang_kuliah', 'Ruang Kuliah'),
        ('ruang_dosen', 'Ruang Dosen'),
        ('lainnya', 'Lainnya'),
    ]

    nama = models.CharField(max_length=150)
    jenis = models.CharField(max_length=20, choices=JENIS_CHOICES, default='laboratorium')
    deskripsi = models.TextField(blank=True)
    foto = models.ImageField(upload_to='fasilitas/', blank=True, null=True)
    urutan = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Fasilitas'
        verbose_name_plural = 'Fasilitas'
        ordering = ['urutan', 'nama']

    def __str__(self):
        return self.nama


class Galeri(models.Model):
    judul = models.CharField(max_length=150)
    deskripsi = models.TextField(blank=True)
    foto = models.ImageField(upload_to='galeri/')
    tanggal = models.DateField(default=timezone.now)
    ditampilkan = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Galeri'
        verbose_name_plural = 'Galeri'
        ordering = ['-tanggal']

    def __str__(self):
        return self.judul


class Alumni(models.Model):
    nama = models.CharField(max_length=150)
    nim = models.CharField(max_length=20, blank=True)
    angkatan = models.PositiveIntegerField()
    tahun_lulus = models.PositiveIntegerField()
    pekerjaan = models.CharField(max_length=200, blank=True)
    instansi = models.CharField(max_length=200, blank=True)
    foto = models.ImageField(upload_to='alumni/', blank=True, null=True)
    testimoni = models.TextField(blank=True)
    ditampilkan = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Alumni'
        verbose_name_plural = 'Alumni'
        ordering = ['-tahun_lulus']

    def __str__(self):
        return f'{self.nama} ({self.angkatan})'


class ProfilProdi(models.Model):
    """Singleton model untuk konten statis profil prodi."""
    sejarah = models.TextField()
    visi = models.TextField()
    misi = models.TextField(help_text='Pisahkan tiap misi dengan baris baru')
    tujuan = models.TextField(blank=True)
    akreditasi = models.CharField(max_length=50, default='Baik')
    tahun_berdiri = models.PositiveIntegerField(default=2020)
    jumlah_mahasiswa = models.PositiveIntegerField(default=0)
    jumlah_dosen = models.PositiveIntegerField(default=0)
    email_prodi = models.EmailField(blank=True)
    telepon = models.CharField(max_length=20, blank=True)
    alamat = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Profil Prodi'
        verbose_name_plural = 'Profil Prodi'

    def __str__(self):
        return 'Profil Program Studi Sains Data'

    def get_misi_list(self):
        """Kembalikan daftar misi sebagai list."""
        return [m.strip() for m in self.misi.splitlines() if m.strip()]


class Kontak(models.Model):
    """Pesan masuk dari form kontak."""
    nama = models.CharField(max_length=100)
    email = models.EmailField()
    subjek = models.CharField(max_length=200)
    pesan = models.TextField()
    tanggal = models.DateTimeField(auto_now_add=True)
    sudah_dibaca = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Pesan Kontak'
        verbose_name_plural = 'Pesan Kontak'
        ordering = ['-tanggal']

    def __str__(self):
        return f'{self.nama} — {self.subjek}'

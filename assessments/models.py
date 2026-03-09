from django.db import models
from curriculum.models import MataKuliah, SubCPMK

class Mahasiswa(models.Model):
    nim = models.CharField(max_length=20, unique=True)
    nama = models.CharField(max_length=150)
    angkatan = models.PositiveIntegerField(help_text="Contoh: 2024")

    class Meta:
        verbose_name_plural = "Mahasiswa"

    def __str__(self):
        return f"{self.nim} - {self.nama}"

class Kelas(models.Model):
    mata_kuliah = models.ForeignKey(MataKuliah, on_delete=models.CASCADE, related_name='kelas_dibuka')
    nama_kelas = models.CharField(max_length=10, help_text="Contoh: A, B, atau DS-01")
    tahun_akademik = models.CharField(max_length=20, help_text="Contoh: Ganjil 2025/2026")
    # Jika sistem sudah pakai sistem User/Dosen, bisa ditambahkan:
    # dosen_pengampu = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name_plural = "Kelas Perkuliahan"

    def __str__(self):
        return f"{self.mata_kuliah.nama} - Kelas {self.nama_kelas} ({self.tahun_akademik})"

class PesertaKelas(models.Model):
    """Tabel ini mewakili KRS mahasiswa untuk kelas tertentu"""
    kelas = models.ForeignKey(Kelas, on_delete=models.CASCADE, related_name='peserta')
    mahasiswa = models.ForeignKey(Mahasiswa, on_delete=models.CASCADE, related_name='kelas_diikuti')

    class Meta:
        verbose_name_plural = "Peserta Kelas"
        unique_together = ('kelas', 'mahasiswa') # Mencegah mahasiswa terdaftar 2x di kelas yang sama

    def __str__(self):
        return f"{self.mahasiswa.nama} | {self.kelas}"

class NilaiSubCPMK(models.Model):
    """Tabel untuk menyimpan skor 0-100 pada setiap Sub-CPMK"""
    peserta = models.ForeignKey(PesertaKelas, on_delete=models.CASCADE, related_name='nilai_subcpmk')
    sub_cpmk = models.ForeignKey(SubCPMK, on_delete=models.CASCADE)
    
    # Dosen menginput nilai mentah skala 0-100 di sini
    nilai_angka = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=0.00,
        help_text="Nilai skala 0-100"
    )

    class Meta:
        verbose_name_plural = "Nilai Sub-CPMK"
        unique_together = ('peserta', 'sub_cpmk') # 1 Mahasiswa hanya punya 1 nilai per Sub-CPMK

    def __str__(self):
        return f"Nilai {self.sub_cpmk.kode} - {self.peserta.mahasiswa.nama}"

    @property
    def nilai_terbobot(self):
        """
        Fitur ini menghitung otomatis kontribusi nilai terhadap CPL/MK
        Rumus: (Nilai Angka / 100) * Bobot Persentase Sub-CPMK
        """
        return (self.nilai_angka / 100) * self.sub_cpmk.bobot_persentase
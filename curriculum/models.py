from django.db import models

class ProfilLulusan(models.Model):
    kode = models.CharField(max_length=10, unique=True, help_text="Contoh: PL01")
    nama = models.CharField(max_length=100, help_text="Contoh: Data Scientist, AI Engineer")
    deskripsi = models.TextField()

    class Meta:
        verbose_name_plural = "Profil Lulusan"

    def __str__(self):
        return f"{self.kode} - {self.nama}"

class CPL(models.Model):
    kode = models.CharField(max_length=10, unique=True, help_text="Contoh: PLO1 atau CPL01")
    deskripsi = models.TextField()
    # Relasi Many-to-Many ke Profil Lulusan
    profil_lulusan = models.ManyToManyField(
        ProfilLulusan, 
        related_name='cpl_terkait',
        help_text="Pilih profil lulusan yang ditunjang oleh CPL ini"
    )

    class Meta:
        verbose_name_plural = "Capaian Pembelajaran Lulusan (CPL)"

    def __str__(self):
        return f"{self.kode}"

class MataKuliah(models.Model):
    kode = models.CharField(max_length=20, unique=True)
    nama = models.CharField(max_length=150, help_text="Contoh: Pengantar Sains Data")
    sks = models.PositiveIntegerField(default=3)
    semester = models.PositiveIntegerField()
    deskripsi = models.TextField()

    class Meta:
        verbose_name_plural = "Mata Kuliah"

    def __str__(self):
        return f"{self.kode} - {self.nama}"

class RPS(models.Model):
    # RPS tetap merujuk ke Mata Kuliah sebagai dokumen rencana eksekusinya
    mata_kuliah = models.OneToOneField(MataKuliah, on_delete=models.CASCADE, related_name='rps')
    tanggal_penyusunan = models.DateField()
    deskripsi = models.TextField()
    
    class Meta:
        verbose_name_plural = "Rencana Pembelajaran Semester (RPS)"

    def __str__(self):
        return f"RPS - {self.mata_kuliah.nama}"

class CPMK(models.Model):
    # CPMK melekat pada Mata Kuliah (bukan RPS) agar bisa di-inline di halaman Mata Kuliah
    mata_kuliah = models.ForeignKey(MataKuliah, on_delete=models.CASCADE, related_name='cpmk')
    kode = models.CharField(max_length=10, help_text="Contoh: CPMK 1")
    deskripsi = models.TextField()
    # Relasi Many-to-Many karena 1 CPMK bisa mendukung beberapa CPL
    cpl = models.ManyToManyField(CPL, related_name='cpmk_terkait')

    class Meta:
        verbose_name_plural = "Capaian Pembelajaran Mata Kuliah (CPMK)"

    def __str__(self):
        return f"{self.kode} ({self.mata_kuliah.kode})"

class SubCPMK(models.Model):
    # Sub-CPMK melekat pada CPMK
    cpmk = models.ForeignKey(CPMK, on_delete=models.CASCADE, related_name='sub_cpmk')
    kode = models.CharField(max_length=15, help_text="Contoh: Sub-CPMK 1")
    deskripsi = models.TextField()
    
    bentuk_penilaian = models.CharField(
        max_length=50, 
        blank=True, 
        null=True, 
        help_text="Contoh: Tugas, Case Method (CM), Quiz, MID, FINAL"
    )
    
    bobot_persentase = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        help_text="Bobot Sub-CPMK terhadap mata kuliah dalam persen (%)"
    )

    class Meta:
        verbose_name_plural = "Sub-CPMK"

    def __str__(self):
        return f"{self.kode} - {self.cpmk.mata_kuliah.kode}"
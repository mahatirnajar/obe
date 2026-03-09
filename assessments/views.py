import os
import pandas as pd
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Kelas, PesertaKelas, NilaiSubCPMK, Mahasiswa, PesertaKelas
from curriculum.models import SubCPMK

def grading_spreadsheet(request, kelas_id):
    kelas = get_object_or_404(Kelas, id=kelas_id)
    peserta_kelas = kelas.peserta.select_related('mahasiswa').all().order_by('mahasiswa__nim')
    sub_cpmk_list = SubCPMK.objects.filter(
        cpmk__mata_kuliah=kelas.mata_kuliah
    ).select_related('cpmk').order_by('cpmk__kode', 'kode')

    # --- LOGIKA UNTUK MENYIMPAN NILAI (JIKA DOSEN KLIK SAVE) ---
    if request.method == 'POST':
        for key, value in request.POST.items():
            # Format nama input kita nanti adalah: nilai_{peserta_id}_{sub_cpmk_id}
            if key.startswith('nilai_') and value != '':
                parts = key.split('_')
                if len(parts) == 3:
                    p_id = int(parts[1])
                    s_id = int(parts[2])
                    
                    # Simpan atau update nilainya
                    NilaiSubCPMK.objects.update_or_create(
                        peserta_id=p_id,
                        sub_cpmk_id=s_id,
                        defaults={'nilai_angka': value}
                    )
        
        messages.success(request, 'Nilai berhasil disimpan!')
        return redirect('assessments:grading_spreadsheet', kelas_id=kelas.id)

    # --- LOGIKA UNTUK MENAMPILKAN NILAI YANG SUDAH ADA ---
    # Kita buat dictionary untuk memetakan nilai agar mudah dipanggil di HTML
    # Format: nilai_dict[peserta_id][sub_cpmk_id] = nilai_angka
    nilai_dict = {}
    semua_nilai = NilaiSubCPMK.objects.filter(peserta__kelas=kelas)
    for n in semua_nilai:
        if n.peserta.id not in nilai_dict:
            nilai_dict[n.peserta.id] = {}
        nilai_dict[n.peserta.id][n.sub_cpmk.id] = n.nilai_angka

    context = {
        'kelas': kelas,
        'peserta_kelas': peserta_kelas,
        'sub_cpmk_list': sub_cpmk_list,
        'nilai_dict': nilai_dict,
    }
    
    return render(request, 'assessments/grading_spreadsheet.html', context)


from curriculum.models import CPL

def cpl_report(request, kelas_id):
    kelas = get_object_or_404(Kelas, id=kelas_id)
    peserta_kelas = kelas.peserta.select_related('mahasiswa').all().order_by('mahasiswa__nim')
    
    # 1. Ambil daftar CPL yang dituju oleh mata kuliah ini
    cpl_list = CPL.objects.filter(cpmk_terkait__mata_kuliah=kelas.mata_kuliah).distinct().order_by('kode')
    
    # 2. Hitung bobot maksimal untuk setiap CPL pada mata kuliah ini
    sub_cpmks = SubCPMK.objects.filter(cpmk__mata_kuliah=kelas.mata_kuliah).prefetch_related('cpmk__cpl')
    cpl_max_weights = {cpl.id: 0 for cpl in cpl_list}
    
    for sub in sub_cpmks:
        for cpl in sub.cpmk.cpl.all():
            if cpl.id in cpl_max_weights:
                cpl_max_weights[cpl.id] += float(sub.bobot_persentase)
                
    # 3. Hitung akumulasi nilai terbobot tiap mahasiswa per CPL
    student_cpl_scores = {p.id: {cpl.id: 0 for cpl in cpl_list} for p in peserta_kelas}
    
    semua_nilai = NilaiSubCPMK.objects.filter(peserta__kelas=kelas).select_related('sub_cpmk')
    for n in semua_nilai:
        peserta_id = n.peserta.id
        sub = n.sub_cpmk
        # Nilai poin riil (misal: 80 * 10% = 8)
        poin_terbobot = float(n.nilai_angka) * (float(sub.bobot_persentase) / 100.0)
        
        for cpl in sub.cpmk.cpl.all():
            if cpl.id in student_cpl_scores.get(peserta_id, {}):
                student_cpl_scores[peserta_id][cpl.id] += poin_terbobot

    # 4. Konversi menjadi Persentase Ketercapaian (Skala 0-100%)
    for p_id in student_cpl_scores:
        for c_id in student_cpl_scores[p_id]:
            max_w = cpl_max_weights[c_id]
            if max_w > 0:
                # Rumus: (Poin / Maksimal Poin CPL) * 100
                persentase = (student_cpl_scores[p_id][c_id] / (max_w / 100.0)) / 100.0
                student_cpl_scores[p_id][c_id] = round(persentase, 2)
            else:
                student_cpl_scores[p_id][c_id] = 0

    context = {
        'kelas': kelas,
        'peserta_kelas': peserta_kelas,
        'cpl_list': cpl_list,
        'cpl_max_weights': cpl_max_weights,
        'student_cpl_scores': student_cpl_scores,
    }
    
    return render(request, 'assessments/cpl_report.html', context)

def upload_peserta_excel(request, kelas_id):
    kelas = get_object_or_404(Kelas, id=kelas_id)
    
    if request.method == 'POST':
        excel_file = request.FILES.get('file_excel')
        
        if not excel_file:
            messages.error(request, 'Silakan pilih file Excel terlebih dahulu.')
        elif not excel_file.name.endswith(('.xls', '.xlsx')):
            messages.error(request, 'Format file tidak valid. Gunakan format .xls atau .xlsx.')
        else:
            # 1. Simpan file secara eksplisit ke folder media sementara
            fs = FileSystemStorage()
            filename = fs.save(excel_file.name, excel_file)
            file_path = fs.path(filename)
            
            try:
                # 2. Baca file dari path yang tersimpan
                df = pd.read_excel(file_path)
                
                required_columns = ['NIM', 'Nama', 'Angkatan']
                if not all(col in df.columns for col in required_columns):
                    messages.error(request, 'Kolom Excel tidak sesuai! Pastikan ada kolom: NIM, Nama, Angkatan')
                    return redirect('assessments:upload_peserta', kelas_id=kelas.id)
                
                mahasiswa_terdaftar = 0
                
                for index, row in df.iterrows():
                    nim = str(row['NIM']).strip()
                    nama = str(row['Nama']).strip()
                    angkatan = int(row['Angkatan']) if pd.notna(row['Angkatan']) else 2024
                    
                    if nim and nim != 'nan':
                        mhs, created = Mahasiswa.objects.get_or_create(
                            nim=nim,
                            defaults={'nama': nama, 'angkatan': angkatan}
                        )
                        if not created:
                            mhs.nama = nama
                            mhs.save()
                            
                        peserta, p_created = PesertaKelas.objects.get_or_create(
                            kelas=kelas, 
                            mahasiswa=mhs
                        )
                        if p_created:
                            mahasiswa_terdaftar += 1
                            
                messages.success(request, f'Berhasil mengimpor {mahasiswa_terdaftar} mahasiswa baru ke kelas {kelas.nama_kelas}.')
                return redirect('admin:assessments_kelas_change', kelas.id)
                
            except Exception as e:
                # Jika terjadi error (misal format file rusak), tampilkan pesan
                messages.error(request, f'Terjadi kesalahan saat memproses file: {e}')
                return redirect('assessments:upload_peserta', kelas_id=kelas.id)
                
            finally:
                # 3. BLOK FINALLY: Ini pasti akan dieksekusi apapun yang terjadi
                # Hapus file Excel dari server agar tidak memenuhi hardisk
                if os.path.exists(file_path):
                    os.remove(file_path)
                
    context = {
        'kelas': kelas
    }
    return render(request, 'assessments/upload_peserta.html', context)
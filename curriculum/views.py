from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .models import MataKuliah

def generate_rps_pdf(request, mk_id):
    # 1. Ambil Data
    mk = get_object_or_404(MataKuliah, id=mk_id)
    cpmk_list = mk.cpmk.all()
    
    # Kumpulkan CPL unik dari CPMK yang ada
    cpl_set = set()
    for cpmk in cpmk_list:
        for cpl in cpmk.cpl.all():
            cpl_set.add(cpl)
            
    context = {
        'mk': mk,
        'cpl_list': list(cpl_set),
        'cpmk_list': cpmk_list,
    }

    # 2. Render HTML
    template = get_template('curriculum/rps_pdf_template.html')
    html = template.render(context)

    # 3. Siapkan Response PDF
    response = HttpResponse(content_type='application/pdf')
    # Gunakan 'attachment;' jika ingin langsung terdownload, atau 'inline;' jika ingin terbuka di tab baru browser
    response['Content-Disposition'] = f'attachment; filename="RPS_{mk.kode}_{mk.nama}.pdf"'

    # 4. Konversi HTML ke PDF
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Terjadi kesalahan saat membuat PDF', status=500)
    
    return response
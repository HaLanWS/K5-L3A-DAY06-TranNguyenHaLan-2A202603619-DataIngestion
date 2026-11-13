import pypdf

r23 = pypdf.PdfReader('data/QCDT-2023-upload.pdf')

def show(p):
    print(f"=== PAGE {p} ===")
    print(' '.join((r23.pages[p-1].extract_text() or '').split())[:1500])

show(8)
show(23)

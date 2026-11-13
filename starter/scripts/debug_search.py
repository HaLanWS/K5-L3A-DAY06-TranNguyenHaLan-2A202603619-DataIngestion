import pypdf

r23 = pypdf.PdfReader('data/QCDT-2023-upload.pdf')
r25 = pypdf.PdfReader('data/QCDT_2025_5445_QD-DHBK.pdf')

def search(r, term):
    found = []
    for idx, p in enumerate(r.pages):
        t = ' '.join((p.extract_text() or '').split())
        if term.lower() in t.lower():
            found.append(idx + 1)
    print(f"'{term}' -> pages {found}")

search(r23, 'hai học kỳ chính')
search(r23, 'thứ hai của chương trình thứ nhất')
search(r23, 'thang điểm 10')
search(r23, '5,5 trở lên')
search(r23, 'trình độ tiến sĩ')
search(r25, 'Điều 23.')
search(r23, 'Điểm đạt:')

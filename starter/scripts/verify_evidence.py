import json
import pypdf

with open('data/benchmark_questions.json', encoding='utf-8') as f:
    qs = json.load(f)

r23 = pypdf.PdfReader('data/QCDT-2023-upload.pdf')
r25 = pypdf.PdfReader('data/QCDT_2025_5445_QD-DHBK.pdf')

print('Verifying evidence for all 20 questions...')
all_ok = True
for q in qs:
    reader = r23 if q['gold_source_id'] == 'QCDT_2023' else r25
    page_text = reader.pages[q['gold_page'] - 1].extract_text() or ''
    norm_page = ' '.join(page_text.split())
    norm_ev = ' '.join(q['evidence_quote'].split())
    if norm_ev in norm_page:
        print(f"OK {q['id']} in {q['gold_source_id']} page {q['gold_page']}")
    else:
        print(f"FAIL {q['id']}: evidence not found in page {q['gold_page']}")
        all_ok = False

if all_ok:
    print('ALL 20 QUESTIONS HAVE 100% VERIFIED GOLD EVIDENCE IN SOURCE PAGES!')

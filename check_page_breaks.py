import docx

doc = docx.Document(r"C:\Users\prajw\.gemini\antigravity\brain\95a2e075-e750-4fba-bd31-a915e83debb4\.user_uploaded\media_1793860029181_098f9158.docx")

p_idx = 0
for i, p in enumerate(doc.paragraphs):
    for r in p.runs:
        if 'w:br' in r._r.xml and 'w:type="page"' in r._r.xml:
            print(f"PAGE BREAK at paragraph {i}: previous text: '{doc.paragraphs[i-1].text[:40]}' -> next text: '{p.text[:40]}'")

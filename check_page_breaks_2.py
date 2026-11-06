import docx

doc = docx.Document(r"C:\Users\prajw\.gemini\antigravity\brain\95a2e075-e750-4fba-bd31-a915e83debb4\.user_uploaded\media_1793860029181_098f9158.docx")

for i, p in enumerate(doc.paragraphs):
    xml = p._p.xml
    if "w:br" in xml:
        print(f"Para {i} has w:br: {p.text[:50]}")
    if "pageBreakBefore" in xml:
        print(f"Para {i} has pageBreakBefore: {p.text[:50]}")

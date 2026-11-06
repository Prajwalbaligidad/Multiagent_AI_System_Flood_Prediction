import docx

doc = docx.Document(r"C:\Users\prajw\.gemini\antigravity\brain\95a2e075-e750-4fba-bd31-a915e83debb4\.user_uploaded\media_1793860029181_098f9158.docx")

print(f"Total paragraphs: {len(doc.paragraphs)}")
print(f"Total tables: {len(doc.tables)}")

for i, p in enumerate(doc.paragraphs):
    xml = p._p.xml
    text = p.text.strip()
    if 'w:br w:type="page"' in xml or 'w:pageBreakBefore' in xml:
        print(f"Break at Para {i}: {text[:60]}")
    elif text.startswith(("1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9.", "10.", "11.", "REFERENCES", "SOURCE CODE", "SUBMISSION PAGE", "PLAGIARISM", "ABSTRACT", "LIST OF SYMBOLS", "CONTENTS", "CERTIFICATE", "DECLARATION", "ACKNOWLEDGEMENT")):
        print(f"Section header at Para {i}: {text[:60]}")

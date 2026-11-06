import docx

doc = docx.Document(r"C:\Users\prajw\.gemini\antigravity\brain\95a2e075-e750-4fba-bd31-a915e83debb4\.user_uploaded\media_1793860029181_098f9158.docx")

for i in range(85, len(doc.paragraphs)):
    t = doc.paragraphs[i].text.strip()
    if t:
        print(f"P{i}: {t[:70]}")

print("\n--- TABLES IN FRIEND DOC ---")
for idx, tbl in enumerate(doc.tables):
    print(f"Table {idx}: rows={len(tbl.rows)}, cols={len(tbl.columns)}, first_cell='{tbl.rows[0].cells[0].text.strip()}'")

import docx

doc = docx.Document(r"C:\Users\prajw\.gemini\antigravity\brain\95a2e075-e750-4fba-bd31-a915e83debb4\.user_uploaded\media_1793860029181_098f9158.docx")

print("DUMPING FRIEND REPORT SECTIONS AND WORD COUNTS:")
curr_section = "PREAMBLE"
sec_text = []

for i, p in enumerate(doc.paragraphs):
    t = p.text.strip()
    if any(t.startswith(prefix) for prefix in ["1. ", "2. ", "3. ", "4. ", "5. ", "6. ", "7. ", "8. ", "9. ", "10. ", "11. ", "REFERENCES", "SOURCE CODE", "SUBMISSION PAGE", "PLAGIARISM REPORT"]):
        if sec_text:
            print(f"[{curr_section}] => {len(' '.join(sec_text).split())} words, {len(sec_text)} paragraphs")
        curr_section = t[:40]
        sec_text = []
    if t:
        sec_text.append(t)

if sec_text:
    print(f"[{curr_section}] => {len(' '.join(sec_text).split())} words, {len(sec_text)} paragraphs")

import docx

doc = docx.Document(r"C:\Users\prajw\.gemini\antigravity\brain\95a2e075-e750-4fba-bd31-a915e83debb4\.user_uploaded\media_1793860029181_098f9158.docx")

print("Checking Certificate (19 to 34):")
for i in range(19, 35):
    print(f"P{i}: '{doc.paragraphs[i].text}'")

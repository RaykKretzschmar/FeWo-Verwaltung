from docx import Document
import datetime

def replace_text(replacements, doc_path="Rechnungsvorlage.docx"):
    doc = Document(doc_path)

    # Go through each paragraph in the document
    for p in doc.paragraphs:
        inline = p.runs
        for i in range(len(inline)):
            for old_text, new_text in replacements.items():
                if old_text in inline[i].text:
                    text = inline[i].text.replace(old_text, new_text)
                    inline[i].text = text

    datum = datetime.datetime.now()
    tag = datum.strftime("%d")
    monat = datum.strftime("%m")
    jahr = datum.strftime("%Y")

    # Save the document
    file_path = f"Rechnung{tag}{monat}{jahr}.docx"
    doc.save(file_path)
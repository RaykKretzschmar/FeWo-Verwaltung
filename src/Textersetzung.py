from docx import Document

def replace_text(old_text, new_text):
    doc = Document("Rechnungsvorlage.docx")  # Fügen Sie hier den Pfad Ihrer Datei ein

    # Geht durch jeden Absatz im Dokument
    for p in doc.paragraphs:
        # Wenn der alte Text im Absatz ist, ersetzen Sie ihn
        if old_text in p.text:
            inline = p.runs
            # Loop added to work with runs (continuous sequence of characters with same style)
            for i in range(len(inline)):
                print(inline[i].text)
                if old_text in inline[i].text:
                    text = inline[i].text.replace(old_text, new_text)
                    inline[i].text = text

    # Speichert das Dokument
    doc.save("neu_Rechnungsvorlage.docx")

replace_text(old_text="Straße", new_text="Dornburger Str.")  # Ersetzt "alter Text" durch "neuer Text"

import tkinter as tk
import csv
import docx
import datetime

class NeuerKundeDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Neuer Kunde")

        self.labels = {
            "Kürzel": tk.StringVar(),
            "Anrede": tk.StringVar(),
            "Vorname": tk.StringVar(),
            "Nachname": tk.StringVar(),
            "Stadt": tk.StringVar(),
            "Postleitzahl": tk.StringVar(),
            "Straße": tk.StringVar(),
            "Hausnummer": tk.StringVar(),
            "Kundennummer": tk.StringVar(),
        }

        for i, (k, v) in enumerate(self.labels.items()):
            tk.Label(self, text=f"{k} : ", anchor="e").grid(row=i, column=0, sticky="e")
            tk.Entry(self, textvariable=v, width=30).grid(row=i, column=1, sticky="ew")

        tk.Button(self, text="Speichern", command=self.save).grid(row=i+1, column=0)
        tk.Button(self, text="Abbrechen", command=self.destroy).grid(row=i+1, column=1)

        self.grid_columnconfigure(1, weight=1)  # make the second column expandable

    def save(self):
        with open('Kunden.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([v.get() for v in self.labels.values()])
        self.destroy()


class AuswahlDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Kunde auswählen")
        self.configure(bg='white')

        self.labels = ["Kürzel", "Anrede", "Vorname", "Nachname", "Stadt", "Postleitzahl", "Straße", "Hausnummer", "Kundennummer"]
        self.checkboxes = []

        for i, label in enumerate(self.labels):
            label_widget = tk.Label(self, text=label, bg='white', fg='black', font=('Arial', 14))
            label_widget.grid(row=0, column=i, sticky='ew')
            self.grid_columnconfigure(i, weight=1)

        with open('Kunden.csv', 'r') as f:
            reader = csv.reader(f)
            for i, line in enumerate(reader, start=1):
                for j, element in enumerate(line):
                    data_widget = tk.Label(self, text=element, bg='white', fg='black', font=('Arial', 12))
                    data_widget.grid(row=i, column=j, sticky='ew')
                checkbox = tk.Checkbutton(self, bg='white')
                checkbox.grid(row=i, column=len(self.labels), sticky='ew')
                self.checkboxes.append(checkbox)
            self.grid_rowconfigure(i, weight=1)

        self.abbruch_button = tk.Button(self, text="Abbrechen", command=self.destroy, fg='black', bg='white', font=('Arial', 12))
        self.abbruch_button.grid(row=i+1, column=0, sticky='ew')

        self.bestätigen_button = tk.Button(self, text="Bestätigen", command=self.bestätigen, fg='black', bg='white', font=('Arial', 12))
        self.bestätigen_button.grid(row=i+1, column=1, sticky='ew')

    def bestätigen(self):
        selected_customers = []
        for i, checkbox in enumerate(self.checkboxes):
            print(i)
            # if checkbox.state():
            #     selected_customers.append(self.data[i])

        for customer in selected_customers:
            replacements = {
                "Kürzel": customer[0],
                "Anrede": customer[1],
                "Vorname": customer[2],
                "Nachname": customer[3],
                "Stadt": customer[4],
                "Postleitzahl": customer[5],
                "Straße": customer[6],
                "Hausnummer": customer[7],
                "Kundennummer": customer[8],
            }
            replace_text(replacements)

        # Then close the dialog
        self.destroy()

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


class VerwaltungListener(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Fewo Kundenverwaltung by Rayk Kretzschmar")
        self.geometry("1600x900")

        self.neuerKundeButton = tk.Button(self, text="Neuer Kunde", command=self.open_neuerKundeDialog)
        self.rechnungButton = tk.Button(self, text="Rechnung erstellen", command=self.open_auswahlDialog)

        self.neuerKundeButton.pack()
        self.rechnungButton.pack()

    def open_neuerKundeDialog(self):
        NeuerKundeDialog(self)

    def open_auswahlDialog(self):
        AuswahlDialog(self)


def main():
    VerwaltungListener().mainloop()

if __name__ == "__main__":
    main()

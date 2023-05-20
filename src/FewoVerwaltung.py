import tkinter as tk
import csv
import Textersetzung

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

        self.labels = ["Kürzel", "Anrede", "Vorname", "Nachname", "Stadt", "PLZ", "Straße", "Hausnummer", "Kundennummer"]
        self.checkboxes = []

        for i, label in enumerate(self.labels):
            label_widget = tk.Label(self, text=label, bg='white', fg='black', font=('Arial', 14))
            label_widget.grid(row=0, column=i, sticky='ew')
            self.grid_columnconfigure(i, weight=1)

        self.checkbutton_vars = []

        with open('Kunden.csv', 'r') as f:
            reader = csv.reader(f)
            for i, line in enumerate(reader, start=1):
                for j, element in enumerate(line):
                    data_widget = tk.Label(self, text=element, bg='white', fg='black', font=('Arial', 12))
                    data_widget.grid(row=i, column=j, sticky='ew')
                
                var = tk.IntVar()
                checkbox = tk.Checkbutton(self, bg='white', variable=var)
                checkbox.grid(row=i, column=len(self.labels), sticky='ew')
                self.checkbutton_vars.append(var)
            self.grid_rowconfigure(i, weight=1)

        self.abbruch_button = tk.Button(self, text="Abbrechen", command=self.destroy, fg='black', bg='white', font=('Arial', 12))
        self.abbruch_button.grid(row=i+1, column=0, sticky='ew')

        self.bestätigen_button = tk.Button(self, text="Bestätigen", command=self.bestätigen, fg='black', bg='white', font=('Arial', 12))
        self.bestätigen_button.grid(row=i+1, column=1, sticky='ew')

    def bestätigen(self):
        selected_rows = [i for i, var in enumerate(self.checkbutton_vars) if var.get() == 1]
        print(f"Selected rows: {selected_rows}")  # Debug print

        with open('Kunden.csv', 'r') as f:
            reader = csv.reader(f)
            for i, line in enumerate(reader):
                if i in selected_rows:
                    replacements = {self.labels[j]: element for j, element in enumerate(line)}
                    print(f"Replacements: {replacements}")  # Debug print
                    Textersetzung.replace_text(replacements)

        self.destroy()


class VerwaltungListener(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Fewo Kundenverwaltung by Rayk Kretzschmar")
        self.geometry("800x600")
        self.configure(bg='white')

        # Adjust font, colors, and padding of the buttons
        self.neuerKundeButton = tk.Button(self, text="Neuer Kunde", command=self.open_neuerKundeDialog, font=('Arial', 14), bg='skyblue', fg='black', padx=10, pady=10)
        self.rechnungButton = tk.Button(self, text="Rechnung erstellen", command=self.open_auswahlDialog, font=('Arial', 14), bg='skyblue', fg='black', padx=10, pady=10)

        # Use grid layout manager and add some margins
        self.neuerKundeButton.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        self.rechnungButton.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

        # Configure the columns and row to expand when the window is resized
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def open_neuerKundeDialog(self):
        NeuerKundeDialog(self)

    def open_auswahlDialog(self):
        AuswahlDialog(self)


def main():
    VerwaltungListener().mainloop()

if __name__ == "__main__":
    main()
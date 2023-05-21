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
        self.configure()

        self.labels = ["Kürzel", "Anrede", "Vorname", "Nachname", "Stadt", "PLZ", "Straße", "Hausnummer", "Kundennummer"]
        self.checkboxes = []

        for i, label in enumerate(self.labels):
            label_widget = tk.Label(self, text=label, font=('Arial', 14))
            label_widget.grid(row=0, column=i, sticky='ew')
            self.grid_columnconfigure(i, weight=1)

        self.selected_data = None  # Store the selected data

        with open('Kunden.csv', 'r') as f:
            reader = csv.reader(f)
            for i, line in enumerate(reader, start=1):
                for j, element in enumerate(line):
                    data_widget = tk.Label(self, text=element, font=('Arial', 12))
                    data_widget.grid(row=i, column=j, sticky='ew')
                
                button = tk.Button(self, text="Rechnung", command=lambda line=line: self.select_data(line))
                button.grid(row=i, column=len(self.labels), sticky='ew')

            self.grid_rowconfigure(i, weight=1)

        self.abbruch_button = tk.Button(self, text="Abbrechen", command=self.destroy, font=('Arial', 12))
        self.abbruch_button.grid(row=i+1, column=0, sticky='ew')

    def select_data(self, data):
        self.selected_data = {self.labels[i]: val for i, val in enumerate(data)}
        EingabeDialog(self, self.selected_data)


class EingabeDialog(tk.Toplevel):
    def __init__(self, parent, data):
        super().__init__(parent)

        self.title("Rechnung erstellen")

        # data should be a dictionary
        for i, (k, v) in enumerate(data.items()):
            tk.Label(self, text=f"{k} : {v}", anchor="e").grid(row=i, column=0, sticky="e")

        self.new_labels = {
            "Datum": tk.StringVar(),
            "Rechnungsnummer": tk.StringVar(),
            "Anreisedatum": tk.StringVar(),
            "Abreisedatum": tk.StringVar(),
            "Name der Ferienwohnung": tk.StringVar(),
            "Preis pro Nacht": tk.StringVar(),
        }

        for j, (k, v) in enumerate(self.new_labels.items(), start=i+1):
            tk.Label(self, text=f"{k} : ", anchor="e").grid(row=j, column=0, sticky="e")
            tk.Entry(self, textvariable=v, width=30).grid(row=j, column=1, sticky="ew")

        tk.Button(self, text="Speichern", command=self.save).grid(row=j+1, column=0)
        tk.Button(self, text="Abbrechen", command=self.destroy).grid(row=j+1, column=1)

        self.grid_columnconfigure(1, weight=1)  # make the second column expandable

    def save(self):
        # Merge selected data and new data
        all_data = {**self.parent.selected_data, **{k: v.get() for k, v in self.new_labels.items()}}

        with open('Kunden.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(all_data.values())
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
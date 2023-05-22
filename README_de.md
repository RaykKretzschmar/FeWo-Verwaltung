# FeWo-Verwaltung (Ferienwohnungs-Verwaltung)

Diese Anwendung wurde mit der Tkinter-Bibliothek von Python erstellt. Sie bietet eine einfache grafische Benutzeroberfläche (GUI) für die Kundenverwaltung eines Ferienwohnungsunternehmens.

Die Anwendung bietet Funktionen zum Hinzufügen neuer Kunden, zur Auswahl eines vorhandenen Kunden aus einer Liste und zur Erstellung einer Rechnung für einen Kunden unter Verwendung einer Word-Dokumentvorlage.



## Voraussetzungen
Bevor Sie die Anwendung ausführen, stellen Sie sicher, dass Sie folgende Anforderungen erfüllen:

1. Python 3.6 oder neuer
2. installierte python-docx Bibliothek: Sie können diese mit pip installieren:
>pip install python-docx



## Funktionen
1. __Neuer Kunde hinzufügen__: Sie können neue Kunden in das System einfügen. Die notwendigen Details umfassen Anrede, Vorname, Nachname, Stadt, Postleitzahl, Straße, Hausnummer und Kundennummer. Eine eindeutige Kundennummer wird automatisch generiert.

2. __Kundenauswahl__: Sie können einen Kunden aus der Liste der in einer CSV-Datei gespeicherten Kunden auswählen. Sie können dann diese Kundendaten verwenden, um eine Rechnung zu erstellen.

3. __Rechnungserstellung__: Sobald ein Kunde ausgewählt ist, können Sie die Details seines Aufenthaltes eingeben, um eine Rechnung zu erstellen. Die notwendigen Details umfassen Datum, Rechnungsnummer, Anreisedatum, Abreisedatum, Name der Ferienwohnung und Preis pro Nacht.

4. __Automatische Preisberechnung__: Die Anwendung berechnet automatisch den Gesamtpreis, die Mehrwertsteuer und den Netto-Betrag basierend auf der Anzahl der Nächte und dem Preis pro Nacht.

5. __Benutzerdefinierte Rechnungsvorlage__: Sie können ein benutzerdefiniertes Word-Dokument als Rechnungsvorlage verwenden. Die Anwendung ersetzt Platzhalter im Dokument durch die tatsächlichen Daten.



## So führen Sie die Anwendung aus
1. Führen Sie das Python-Skript in Ihrem Terminal oder Ihrer Befehlszeile aus:

>python FewoVerwaltung.py
2. Wenn die Anwendung geöffnet ist, klicken Sie auf die Schaltfläche "Neuer Kunde", um einen neuen Kunden hinzuzufügen.

3. Klicken Sie auf die Schaltfläche "Rechnung erstellen", um einen Kunden auszuwählen und eine Rechnung zu erstellen.

4. Sie werden aufgefordert, ein Word-Dokument als Vorlage für die Rechnung anzugeben. Stellen Sie sicher, dass das Dokument Platzhalter enthält, die den Kunden- und Rechnungsdaten entsprechen.

5. Die Anwendung generiert ein Word-Dokument mit dem ersetzen Text und speichert es an dem von Ihnen ausgewählten Ort.



## Hinweis
Diese Anwendung unterstützt nur .docx Word-Dokumente. Das Word-Dokument sollte Platzhalter in Form Ihrer Labels enthalten. Zum Beispiel, wenn Sie ein Label "Anrede" haben, sollte Ihr Word-Dokument einen Platzhalter "Anrede" enthalten, wo diese Information eingef
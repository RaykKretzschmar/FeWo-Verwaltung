# FeWo-Verwaltung (Vacation Rental Management)

This application is built using Python's Tkinter library. It provides a simple Graphical User Interface (GUI) for managing customers of a vacation rental business.

The application provides functionality to add new customers, choose an existing customer from a list, and generate an invoice for a customer using a Word document template.



## Prerequisites
Before running the application, make sure you have the following:

1. Python 3.6 or newer
2. python-docx library installed: This can be installed using pip:
>pip install python-docx



## Features
1. __New Customer Addition__: You can add new customers into the system. The necessary details include Salutation, First Name, Last Name, City, Postal Code, Street, House Number, and Customer Number. A unique customer number is automatically generated.

2. __Customer Selection__: You can select a customer from the list of customers saved in a CSV file. You can then use this customer data to create an invoice.

3. __Invoice Generation__: Once a customer is selected, you can input the details of their stay to generate an invoice. The necessary details include Date, Invoice Number, Arrival Date, Departure Date, Name of the holiday home, and Price per night.

4. __Automatic Price Calculation__: The application automatically calculates the total price, VAT, and net amount based on the number of nights and price per night.

5. __Custom Invoice Template__: You can use a custom Word document as an invoice template. The application will replace placeholders in the document with the actual data.



## How to Run the Application
1. Run the Python script in your terminal or command line:

>python FewoVerwaltung.py
2. When the application opens, click on the "Neuer Kunde" button to add a new customer.

3. Click on the "Rechnung erstellen" button to select a customer and generate an invoice.

4. You will be asked to provide a Word document as a template for the invoice. Make sure the document contains placeholders that match the customer and invoice data.

5. The application will generate a Word document with the replaced text and save it in your chosen location.



## Note
This application only supports .docx Word documents. The Word document should contain placeholders in the form of your labels. For example, if you have a label "Anrede", your Word document should contain a placeholder "Anrede" where you want this information to be inserted.
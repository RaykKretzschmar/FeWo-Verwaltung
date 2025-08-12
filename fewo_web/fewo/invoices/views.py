from django.shortcuts import render, redirect, get_object_or_404
from .models import Invoice
from .forms import InvoiceForm
from customers.models import Customer
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
from django.core.files.base import File


def invoice_list(request):
    invoices = Invoice.objects.all()
    return render(request, "invoices/invoice_list.html", {"invoices": invoices})


@login_required
def invoice_create(request):
    if request.method == "POST":
        form = InvoiceForm(request.POST)
        if form.is_valid():
            invoice = form.save()
            generate_invoice_pdf(invoice)
            return redirect("invoice_list")
    else:
        form = InvoiceForm()
    return render(request, "invoices/invoice_form.html", {"form": form})


def generate_invoice_pdf(invoice: Invoice):
    # Render HTML
    html_string = render_to_string(
        "invoices/invoice_template.html", {"invoice": invoice}
    )
    html = HTML(string=html_string)

    # Create temp file and write PDF
    result = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    html.write_pdf(result.name)

    # Save to model FileField
    with open(result.name, "rb") as f:
        django_file = File(f)
        invoice.pdf_file.save(
            f"invoice_{invoice.invoice_number}.pdf", django_file, save=True
        )


@login_required
def invoice_create_for_customer(request, customer_id=None):
    customer = None
    if customer_id:
        customer = get_object_or_404(Customer, id=customer_id)

    if request.method == "POST":
        form = InvoiceForm(request.POST)
        if form.is_valid():
            invoice = form.save(commit=False)
            if customer:
                invoice.customer = customer
            invoice.save()
            generate_invoice_pdf(invoice)
            return redirect("invoice_list")
    else:
        initial = {}
        if customer:
            initial["customer"] = customer
        form = InvoiceForm(initial=initial)

    return render(
        request, "invoices/invoice_form.html", {"form": form, "customer": customer}
    )

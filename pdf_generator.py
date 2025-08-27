# pdf_generator.py
from fpdf import FPDF
from datetime import datetime
import random
import os
import qrcode
from num2words import num2words


def generate_pdf(
    customer_name,
    customer_phone,
    customer_address,
    services,
    template="classic",
    tax_rate=10,
    company=None,
    logo_path="logo.png",
    payment_url=None,
):
    """
    Generate a professional PDF quote with branding, tax, QR code, and modern design.

    Returns a dict: {filename, quote_number, subtotal, tax, total}
    """
    # Defaults
    company = company or {
        "name": "STAR CAR WASH (MELBOURNE) PTY LTD",
        "email": "info@starcarwash.com.au",
        "phone": "0474456050",
    }
    if not os.path.exists("quotes"):
        os.makedirs("quotes")

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # --- Header / Logo ---
    if logo_path and os.path.exists(logo_path):
        pdf.image(logo_path, 10, 8, 28)

    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, company["name"], ln=True, align="C")
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 6, f"Email: {company['email']} | Phone: {company['phone']}", ln=True, align="C")
    pdf.ln(8)

    # --- Quote metadata ---
    quote_number = f"Q-{datetime.now().strftime('%Y%m%d')}-{random.randint(100,999)}"
    date_str = datetime.now().strftime("%d %b %Y")

    pdf.set_font("Arial", size=10)
    pdf.cell(100, 6, f"Quote Number: {quote_number}", ln=0, align="L")
    pdf.cell(90, 6, f"Date: {date_str}", ln=1, align="R")
    pdf.ln(3)

    # --- Customer Details ---
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 8, "Bill To:", ln=True, align="L")
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 6, customer_name or "-", ln=True, align="L")
    pdf.cell(200, 6, f"Phone: {customer_phone or '-'}", ln=True, align="L")
    pdf.multi_cell(200, 6, f"Address: {customer_address or '-'}", align="L")
    pdf.ln(5)

    # --- Table Header ---
    if template == "modern":
        pdf.set_font("Arial", "B", 11)
        pdf.set_fill_color(50, 50, 150)
        pdf.set_text_color(255, 255, 255)
    else:
        pdf.set_font("Arial", "B", 11)
        pdf.set_fill_color(200, 200, 200)
        pdf.set_text_color(0, 0, 0)

    pdf.cell(10, 8, "QTY", border=1, align="C", fill=True)
    pdf.cell(60, 8, "Service", border=1, align="C", fill=True)
    pdf.cell(60, 8, "Description", border=1, align="C", fill=True)
    pdf.cell(30, 8, "Price", border=1, align="C", fill=True)
    pdf.cell(30, 8, "Final", border=1, align="C", fill=True)
    pdf.ln()

    # --- Table Rows ---
    pdf.set_font("Arial", size=10)
    subtotal = 0.0

    for svc in services:
        name = (svc.get("name") or "")[:34]
        desc = (svc.get("description") or "")[:36]
        price = float(svc.get("price") or 0.0)
        discount = float(svc.get("discount") or 0.0)
        final = price - (price * discount / 100.0)
        subtotal += final

        pdf.cell(10, 8, "1", border=1, align="C")
        pdf.cell(60, 8, name, border=1)
        pdf.cell(60, 8, desc, border=1)
        pdf.cell(30, 8, f"${price:.2f}", border=1, align="R")
        pdf.cell(30, 8, f"${final:.2f}", border=1, align="R")
        pdf.ln()

    # --- Totals ---
    tax_amount = (subtotal * (tax_rate or 0)) / 100.0
    grand_total = subtotal + tax_amount

    pdf.set_font("Arial", "B", 11)
    pdf.cell(160, 8, "Subtotal (AUD)", border=1, align="R")
    pdf.cell(30, 8, f"${subtotal:.2f}", border=1, align="R")
    pdf.ln()

    pdf.cell(160, 8, f"Tax ({tax_rate or 0}%)", border=1, align="R")
    pdf.cell(30, 8, f"${tax_amount:.2f}", border=1, align="R")
    pdf.ln()

    pdf.cell(160, 8, "Grand Total (AUD)", border=1, align="R")
    pdf.cell(30, 8, f"${grand_total:.2f}", border=1, align="R")
    pdf.ln(8)

    # Amount in words
    try:
        words = num2words(grand_total, to="currency", lang="en")
        pdf.set_font("Arial", "I", 9)
        pdf.multi_cell(0, 6, f"Amount in words: {words.capitalize()}")
        pdf.ln(2)
    except Exception:
        pass

    # --- QR code (optional payment link) ---
    if payment_url:
        qr = qrcode.make(f"{payment_url}?quote={quote_number}&amount={grand_total:.2f}")
        qr_path = f"quotes/{quote_number}_qr.png"
        qr.save(qr_path)
        # Show near bottom-right
        y = pdf.get_y() + 2
        if y > 240:  # avoid footer overlap
            pdf.add_page()
            y = 30
        pdf.image(qr_path, x=170, y=y, w=25)
    else:
        qr_path = None

    # --- Notes & Footer ---
    pdf.set_font("Arial", size=9)
    pdf.multi_cell(0, 6, "Notes:\n- This quote is valid for 30 days.\n- Payment due upon completion of service.")

    pdf.set_y(-18)
    pdf.set_font("Arial", "I", 9)
    pdf.cell(0, 6, "Thank you for choosing us.", align="C")

    filename = f"quotes/quote_{quote_number}.pdf"
    pdf.output(filename)

    # Cleanup temp QR
    if qr_path and os.path.exists(qr_path):
        try:
            os.remove(qr_path)
        except Exception:
            pass

    return {
        "filename": filename,
        "quote_number": quote_number,
        "subtotal": round(subtotal, 2),
        "tax": round(tax_amount, 2),
        "total": round(grand_total, 2),
    }

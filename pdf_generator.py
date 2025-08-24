from fpdf import FPDF

def generate_pdf(customer_name, customer_phone, customer_address, service_request, total_price):
    # Create a PDF object
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Add content to the PDF
    pdf.cell(200, 10, txt="STAR CAR WASH (MELBOURNE) PTY LTD", ln=True, align="C")
    pdf.cell(200, 10, txt="Email: info@starcarwash.com.au", ln=True, align="C")
    pdf.cell(200, 10, txt="Phone: 0474456050", ln=True, align="C")
    pdf.cell(200, 10, txt="Bill To:", ln=True, align="L")
    pdf.cell(200, 10, txt=f"{customer_name}", ln=True, align="L")
    pdf.cell(200, 10, txt=f"Phone: {customer_phone}", ln=True, align="L")
    pdf.cell(200, 10, txt=f"Address: {customer_address}", ln=True, align="L")
    pdf.cell(200, 10, txt="QTY Description", ln=True, align="L")
    pdf.cell(200, 10, txt=f"1.00 {service_request}", ln=True, align="L")
    pdf.cell(200, 10, txt=f"Total (AUD): ${total_price}", ln=True, align="L")

    # Save the PDF
    pdf.output("quote.pdf")
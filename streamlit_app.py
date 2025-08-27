# streamlit_app.py
import os
from datetime import datetime
import streamlit as st
from pdf_generator import generate_pdf
from email_utils import send_email_with_attachment
from db import init_db, save_quote, list_quotes

st.set_page_config(page_title="AI-Powered Quote Generator", page_icon="🧾", layout="wide")
init_db()

st.title("🧾 AI-Powered Quote Generator")

# ---------------- Sidebar: Company Settings ----------------
st.sidebar.header("🏢 Company Settings")

company_name = st.sidebar.text_input("Company Name", value="STAR CAR WASH (MELBOURNE) PTY LTD")
company_email = st.sidebar.text_input("Company Email", value="info@starcarwash.com.au")
company_phone = st.sidebar.text_input("Company Phone", value="0474456050")
tax_rate = st.sidebar.slider("Tax Rate (%)", min_value=0, max_value=28, value=10)
template = st.sidebar.selectbox("PDF Template", ["classic", "modern"])
payment_url = st.sidebar.text_input("Payment / Website URL (for QR)", value="https://starcarwash.com.au/pay")

logo_file = st.sidebar.file_uploader("Upload Logo (PNG/JPG)", type=["png", "jpg", "jpeg"])
logo_path = "logo.png"
if logo_file is not None:
    with open(logo_path, "wb") as f:
        f.write(logo_file.read())
    st.sidebar.success("Logo uploaded.")

company = {
    "name": company_name,
    "email": company_email,
    "phone": company_phone,
}

# ---------------- Main Form ----------------
st.subheader("👤 Customer Information")

col1, col2 = st.columns(2)
with col1:
    customer_name = st.text_input("Customer Name", value="")
    customer_phone = st.text_input("Phone Number", value="")
with col2:
    customer_address = st.text_input("Address", value="")

st.subheader("🛠️ Service Request")
service_count = st.number_input("How many services?", min_value=1, max_value=10, value=3, step=1)

services = []
for i in range(service_count):
    with st.expander(f"Service {i+1}", expanded=(i == 0)):
        name = st.text_input(f"Service Name {i+1}", value="Digital marketing package", key=f"name_{i}")
        desc = st.text_area(f"Description {i+1}", value="SEO, social media management, and ads campaign.", key=f"desc_{i}")
        price = st.number_input(f"Price (AUD) {i+1}", min_value=0.0, value=8000.0, step=50.0, key=f"price_{i}")
        discount = st.number_input(f"Discount (%) {i+1}", min_value=0.0, max_value=100.0, value=0.0, step=1.0, key=f"disc_{i}")
        services.append({"name": name, "description": desc, "price": price, "discount": discount})

# Preview total
preview_total = sum(s["price"] - (s["price"] * s["discount"] / 100.0) for s in services)
st.info(f"💰 Estimated Subtotal (before tax): AUD ${preview_total:.2f}")

# ---------------- Generate PDF ----------------
if st.button("📄 Generate Quote PDF"):
    if not services:
        st.error("Please add at least one service.")
    else:
        result = generate_pdf(
            customer_name=customer_name,
            customer_phone=customer_phone,
            customer_address=customer_address,
            services=services,
            template=template,
            tax_rate=tax_rate,
            company=company,
            logo_path=logo_path if os.path.exists(logo_path) else None,
            payment_url=payment_url if payment_url.strip() else None,
        )
        st.success("✅ Quote generated successfully!")
        st.write(f"**Quote Number:** {result['quote_number']}")
        st.write(f"**Subtotal:** ${result['subtotal']:.2f} | **Tax:** ${result['tax']:.2f} | **Grand Total:** ${result['total']:.2f}")

        # Save in DB
        save_quote({
            "quote_number": result["quote_number"],
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "customer_name": customer_name,
            "phone": customer_phone,
            "address": customer_address,
            "subtotal": result["subtotal"],
            "tax": result["tax"],
            "total": result["total"],
            "pdf_path": result["filename"],
        })

        # Download button
        with open(result["filename"], "rb") as f:
            st.download_button("⬇️ Download PDF", f, file_name=os.path.basename(result["filename"]))

        st.session_state["last_pdf"] = result["filename"]

# ---------------- Email PDF Section ----------------
st.subheader("✉️ Email this Quote (Optional)")
colE1, colE2 = st.columns(2)
with colE1:
    smtp_host = st.text_input("SMTP Host", value="smtp.gmail.com")
    smtp_port = st.number_input("SMTP Port", value=587, step=1)
    smtp_user = st.text_input("SMTP Username (email)", value="")
    smtp_pass = st.text_input("SMTP Password / App Password", value="", type="password")
with colE2:
    sender_email = st.text_input("Sender Email", value="")
    to_email = st.text_input("Recipient Email", value="")
    email_subject = st.text_input("Email Subject", value="Your Quote")
    email_body = st.text_area("Email Body", value="Hello,\n\nPlease find attached your quote.\n\nThanks.")

if st.button("📧 Send Email with PDF"):
    pdf_path = st.session_state.get("last_pdf")
    if not pdf_path or not os.path.exists(pdf_path):
        st.error("No PDF found. Please generate a quote first.")
    elif not (smtp_host and smtp_port and smtp_user and smtp_pass and sender_email and to_email):
        st.error("Please fill all SMTP and email fields.")
    else:
        try:
            send_email_with_attachment(
                smtp_host=str(smtp_host),
                smtp_port=int(smtp_port),
                smtp_user=str(smtp_user),
                smtp_pass=str(smtp_pass),
                sender_email=str(sender_email),
                to_email=str(to_email),
                subject=str(email_subject),
                body=str(email_body),
                attachment_path=pdf_path,
            )
            st.success(f"✅ Email sent to {to_email}")
        except Exception as e:
            st.error(f"Failed to send email: {e}")

# ---------------- Past Quotes ----------------
st.subheader("🗂️ Recent Quotes")
rows = list_quotes(limit=10)
if not rows:
    st.write("No quotes saved yet.")
else:
    for qn, dt, cname, total, path in rows:
        cols = st.columns([2, 2, 2, 2, 2])
        cols[0].write(f"**{qn}**")
        cols[1].write(dt)
        cols[2].write(cname or "-")
        cols[3].write(f"${total:.2f}")
        if os.path.exists(path):
            with open(path, "rb") as f:
                cols[4].download_button("⬇️ Download", f, file_name=os.path.basename(path), key=path)
        else:
            cols[4].write("Missing file")

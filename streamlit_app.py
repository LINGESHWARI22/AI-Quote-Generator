# streamlit_app.py
import streamlit as st
from quote_generator import generate_quote
from pdf_generator import generate_pdf

# Streamlit app title
st.title("AI-Powered Quote Generator")

# ----------------------
# User Input
# ----------------------
customer_name = st.text_input("Customer Name:")
customer_phone = st.text_input("Customer Phone:")
customer_address = st.text_input("Customer Address:")
service_request = st.text_input("Describe the service required:")

# ----------------------
# Generate Quote Button
# ----------------------
if st.button("Generate Quote"):
    # Get the service quote from the AI generator
    service = generate_quote(service_request)  # returns a dict with 'name', 'price', 'description'

    if service:
        # Display customer details
        st.write("### Customer Details")
        st.write(f"**Name:** {customer_name}")
        st.write(f"**Phone:** {customer_phone}")
        st.write(f"**Address:** {customer_address}")

        # Display the generated quote
        st.write("### Generated Quote")
        st.write(f"👉 {service['name']}")
        st.write(f"💰 Price: ₹{service['price']}")
        st.write(f"📝 Description: {service['description']}")

        # Generate PDF with the actual service price
        total_price = service['price']
        generate_pdf(customer_name, customer_phone, customer_address, service['name'], total_price)

        # Provide a download link for the PDF
        with open("quote.pdf", "rb") as f:
            st.download_button("Download Quote", f, file_name="quote.pdf")
    else:
        # No service found
        st.write("❌ Sorry, no matching service found.")

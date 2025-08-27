# 🚀 AI-Powered Quote Generator – Smart Business Quoting System  

### **Description**  
The **AI-Powered Quote Generator** is an intelligent web application that automates professional service quote creation. It uses **Hugging Face NLP models** to suggest services based on user input, auto-fills pricing/descriptions, and generates **custom-branded PDF quotes**.  

This tool saves businesses time, ensures consistent pricing, and enhances client communication by offering **instant, AI-driven quotes** with email integration.  

---

## **Key Features**  
- 🤖 **AI-Powered Search** – Context-aware service suggestions using Hugging Face Sentence Transformers.  
- 📄 **Dynamic PDF Generation** – Professionally formatted quotes with company branding.  
- 📧 **Email Integration** – Sends quotes directly to clients via Gmail API/SMTP.  
- 💾 **Quote Management** – Stores quote history in SQLite/Chroma DB with unique IDs.  
- 🎨 **Modern Web UI** – Interactive, user-friendly interface built with Streamlit.  
- 🌐 **Deploy Anywhere** – Easy hosting on Streamlit Cloud, Render, or Heroku.  

---

## **Tech Stack**  
- **Frontend:** Streamlit (Python Interactive UI)  
- **Backend:** Python  
- **AI & NLP:** Hugging Face Sentence Transformers (Embeddings)  
- **Database:** SQLite / Chroma Vector DB  
- **PDF Generation:** ReportLab  
- **Email Service:** smtplib / Gmail API  
- **Version Control:** Git, GitHub  
- **Deployment:** Streamlit Cloud / Render / Heroku  

---

## **Project Structure**  
AI-Quote-Generator/
│── data/ # Service data & embeddings
│── embeddings.py # AI semantic search (Hugging Face)
│── quote_generator.py # Core logic for quote creation
│── pdf_generator.py # PDF generation with branding
│── email_service.py # Send quotes via email
│── streamlit_app.py # Web interface
│── requirements.txt # Dependencies
└── README.md


---

## **Setup & Run**  
# Clone Repository
git clone https://github.com/LINGESHWARI22/AI-Quote-Generator.git
cd AI-Quote-Generator

# Setup Virtual Environment
python -m venv venv
venv\Scripts\activate  

# Install Requirements
pip install -r requirements.txt

# Run the App
streamlit run streamlit_app.py

# Open in Browser
http://localhost:8501

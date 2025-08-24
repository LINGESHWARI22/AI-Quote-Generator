AI-Powered Quote Generator

An AI-driven web application that generates professional service quotes instantly using semantic search. The system retrieves the most relevant service details, auto-fills pricing and descriptions, and allows users to download PDF quotes, streamlining client communication and saving time.

🚀 Features
AI-Powered Search – Finds the most relevant service details using Hugging Face embeddings and Chroma DB.
Dynamic Quote Generation – Automatically generates professional quotes based on client input.
PDF Export – Download quotes as PDFs for sharing with clients.
Streamlit Web Interface – Clean and interactive user interface.

🛠 Tech Stack

Frontend: Streamlit (Python)
Backend: Python
AI & NLP: Hugging Face Sentence Transformers
Database: Chroma Vector DB

Others: PDF Generation (ReportLab), Git

📂 Project Structure

├── data/                
├── embeddings.py        
├── quote_generator.py   
├── pdf_generator.py     
├── streamlit_app.py     
├── requirements.txt     
└── README.md            

⚡ Setup Instructions
Clone the Repository
git clone https://github.com/LINGESHWARI22/AI-Quote-Generator.git
cd AI-Quote-Generator


Create Virtual Environment & Install Requirements
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt


Run the App
streamlit run streamlit_app.py


Open in Browser
http://localhost:8501

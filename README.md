EchoRead — AI Reading Companion with Voice
EchoRead turns long reading material into something you can actually finish. Give it an article link, a PDF file, or pasted text, and it extracts the text, generates a clear AI summary that streams in live (word by word, like ChatGPT), explains the difficult key terms inline, and can read the summary aloud to you.
Built with FastAPI, MySQL, and vanilla HTML/CSS/JavaScript.
Features
Three ways to add a document — paste an article URL, upload a PDF, or paste raw text
Automatic text extraction — clean article text from web pages (ads and menus removed), and full text extraction from PDFs
Streaming AI summary — the summary is generated and streamed to the page live using Server-Sent Events, instead of making the user wait for a spinner
Key-term explanations — important/difficult terms in the text are identified with short, simple meanings, shown on hover
Read aloud — text-to-speech converts the summary into an audio file you can play in the browser
Reading library — every document is saved in MySQL with its original text, summary, and key terms, so your reading history is always there when you come back
Tech Stack
Layer
Technology
Backend
Python, FastAPI
Server
Uvicorn
Database
MySQL 8, SQLAlchemy ORM, PyMySQL
PDF extraction
PyMuPDF
Web article extraction
trafilatura, BeautifulSoup, Requests
Text-to-speech
edge-tts
Live streaming
Server-Sent Events (FastAPI StreamingResponse)
Frontend
HTML, CSS, JavaScript (no framework)
How It Works
The user submits a URL, a PDF, or pasted text.
extractor.py pulls the clean text out of the source.
The document is saved in the documents table in MySQL.
ai_service.py sends the text to the AI model, which returns a summary and a set of key terms with simple explanations.
The summary streams back to the browser live over SSE while it is being generated, then the final summary and key terms are saved against the document.
On request, tts_service.py converts the summary to speech and saves the audio file for playback.
Project Structure
echoread/
├── .env               # Local configuration and secrets (never committed)
├── requirements.txt   # Python dependencies
├── database.py        # MySQL connection, engine, session handling
├── models.py          # SQLAlchemy model — documents table
├── schemas.py         # Pydantic request/response schemas
├── extractor.py       # Text extraction from URLs (trafilatura/BeautifulSoup) and PDFs (PyMuPDF)
├── ai_service.py      # AI summary generation and key-term extraction
├── tts_service.py     # Text-to-speech audio generation (edge-tts)
├── main.py            # FastAPI app — routes, SSE streaming, background tasks
├── index.html         # Frontend — single page UI
├── style.css          # Frontend styling
├── app.js             # Frontend logic — submit, stream, hover terms, audio playback
├── uploads/           # Uploaded PDF files
└── audio_outputs/     # Generated speech audio files
Getting Started
Prerequisites
Python 3.10+
MySQL Server 8 running locally
1. Clone the repository
git clone https://github.com/MahamFatima01713/echoread.git
cd echoread
2. Create and activate a virtual environment
Windows (PowerShell):
python -m venv venv
.\venv\Scripts\Activate.ps1
macOS / Linux:
python -m venv venv
source venv/bin/activate
3. Install dependencies
pip install -r requirements.txt
4. Create the database
In MySQL Workbench (or the MySQL CLI):
CREATE DATABASE echoread_db;
5. Configure environment variables
Create a .env file in the project root:
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_mysql_password
MYSQL_DB=echoread_db
AI_API_KEY=your_ai_api_key
Variable
Description
MYSQL_HOST
MySQL server host
MYSQL_USER
MySQL username
MYSQL_PASSWORD
MySQL password
MYSQL_DB
Database name (echoread_db)
AI_API_KEY
API key for the AI model used for summaries and key terms
The .env file contains secrets. It is listed in .gitignore and must never be committed.
6. Run the backend
uvicorn main:app --reload
The API is now running at http://127.0.0.1:8000. Interactive API documentation (Swagger UI) is available at http://127.0.0.1:8000/docs.
7. Open the frontend
Open index.html in your browser. Add a document, watch the summary stream in, hover the highlighted terms for their meanings, and press play to listen.
API Endpoints
Method
Endpoint
Description
POST
/documents/url
Add a document from an article URL
POST
/documents/upload
Add a document by uploading a PDF file
POST
/documents/text
Add a document from pasted text
GET
/documents
List all saved documents
GET
/documents/{document_id}
Get one document with its summary and key terms
DELETE
/documents/{document_id}
Delete a document
GET
/documents/{document_id}/summary/stream
Stream the AI summary live (Server-Sent Events)
GET
/documents/{document_id}/audio
Generate and return the summary as speech audio
Database Schema
Single table — documents:
Column
Type
Description
id
Integer (PK)
Unique document ID, auto-generated
title
String(255), nullable
Document title
source_type
String(50)
How the document was added: url, pdf, or pasted_text
source_url
String(500), nullable
Original article link (URL documents only)
original_text
Text
Full extracted text of the document
summary
Text, nullable
AI-generated summary (filled after generation)
key_terms
Text, nullable
Key terms with explanations, stored as JSON
created_at
DateTime
When the document was added, set automatically
Roadmap
User accounts and login, so each user has a private library
Choice of AI provider from the settings screen
Redis + Celery background queue for very large documents
Reading progress and bookmarks
Docker setup for one-command deployment
Author
Maham Fatima — BSIT (Final Year), University of the Punjab, Lahore
GitHub: github.com/MahamFatima01713

# HealthAware AI - Health Awareness Chatbot

An AI-driven diagnostic medical assistant and public health awareness chatbot. HealthAware AI is designed to act like a professional healthcare assistant—collecting patient history, suggesting relevant medical specialists, and providing context-grounded public health information using a state-of-the-art Retrieval-Augmented Generation (RAG) pipeline.

## Features

- **Interactive Diagnostic Assistant**: Communicates with users in a concise, "doctor-like" questioning style to understand symptoms and provide relevant medical guidance.
- **Retrieval-Augmented Generation (RAG)**: Uses local vector databases to anchor AI responses in verified medical and public health data, reducing hallucinations.
- **Privacy-First Architecture**: Personal identifiable information (PII) is sanitized locally before being sent to the cloud LLM inference engine.
- **Premium User Interface**: A modern, responsive React frontend with a sleek dark-mode UI for a seamless user experience.
- **Conversational Memory**: Maintains chat context across interactions for a smooth and continuous diagnostic process.

## Tech Stack

### Frontend (User Interface)
- **Framework**: React.js with Vite
- **Styling**: Vanilla CSS (Premium Dark Mode Aesthetics)
- **HTTP Client**: Axios
- **Markdown Parsing**: `react-markdown` for rendering formatted AI responses
- **Icons**: `lucide-react`
- **Hosting**: Vercel

### Backend (API & AI Pipeline)
- **Framework**: FastAPI (Python)
- **Vector Database**: ChromaDB (Local vector storage)
- **Embeddings**: `sentence-transformers` for local document embedding
- **LLM Engine**: Groq Cloud API (Lightning-fast inference for conversational AI)
- **Orchestration**: LangChain for managing the RAG pipeline
- **Hosting**: Render

## Project Structure

This repository is organized as a monorepo:

```text
├── backend/            # FastAPI server, RAG pipeline, and vector DB setup
│   ├── app/            # Application logic, routers, and configuration
│   ├── data/           # Health document corpus for RAG
│   ├── scripts/        # Ingestion scripts for populating the vector DB
│   ├── main.py         # FastAPI application entry point
│   └── requirements.txt# Python dependencies
├── frontend/           # React + Vite frontend application
│   ├── public/         # Static assets
│   ├── src/            # React components, styles, and API clients
│   └── package.json    # Node dependencies and scripts
├── DEPLOYMENT.md       # Cloud deployment instructions
└── render.yaml         # Blueprint for Render deployment
```

## Getting Started (Local Development)

### Prerequisites
- Node.js (v18+)
- Python (3.10+)
- Groq API Key

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # Windows:
   .\venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables:
   Copy `.env.example` to `.env` and add your `GROQ_API_KEY`.
5. Ingest the health data into ChromaDB:
   ```bash
   python scripts/ingest.py
   ```
6. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Set up environment variables:
   Copy `.env.example` to `.env` and configure `VITE_API_BASE_URL` (e.g., `http://localhost:8000`).
4. Start the Vite development server:
   ```bash
   npm run dev
   ```

## Deployment

For detailed deployment instructions for Render (Backend) and Vercel (Frontend), please refer to the [DEPLOYMENT.md](./DEPLOYMENT.md) guide.

# Deployment Guide

This repo is a monorepo:

- `backend/`: FastAPI + local ChromaDB retrieval + Groq generation
- `frontend/`: React/Vite chat UI

Use GitHub for source control, Render for the backend, and Vercel for the frontend.

## Backend: Render

1. Push this repository to GitHub.
2. In Render, create a new Blueprint or Web Service from the GitHub repo.
3. If using the included `render.yaml`, Render reads the backend settings automatically.
4. Add the secret environment variable:

   ```env
   GROQ_API_KEY=your_groq_api_key
   ```

5. Deploy.

The backend build runs:

```bash
pip install -r requirements.txt && python scripts/ingest.py
```

The backend start command is:

```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

After deploy, test:

```text
https://your-render-service.onrender.com/health
```

## Frontend: Vercel

1. Import the same GitHub repo into Vercel.
2. Set the project root directory to `frontend`.
3. Use the default Vite settings:
   - Build command: `npm run build`
   - Output directory: `dist`
4. Add this environment variable:

   ```env
   VITE_API_BASE_URL=https://your-render-service.onrender.com
   ```

5. Deploy.

## Important

- Never commit `backend/.env`; it contains secrets.
- If a real API key is ever pushed to GitHub, rotate it immediately in Groq.
- For stricter production CORS, replace `CORS_ORIGINS=*` on Render with your Vercel URL.

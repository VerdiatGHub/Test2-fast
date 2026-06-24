# NeuralAgent

NeuralAgent is an AI agent that lives on your desktop and completes tasks for you. Describe what you want in plain English and the agent plans the work, looks at your screen, and drives the mouse and keyboard to get it done.

## Architecture

- **backend/** — FastAPI service (PostgreSQL + Alembic). Hosts the LLM-powered agents: task classifier, planner, computer-use (vision) agent, title and suggestion generators.
- **desktop/** — Electron desktop app (React frontend in `neuralagent-app/`) plus the Python automation loop in `aiagent/` that captures the screen and executes actions with PyAutoGUI / UIAutomation.
- **docs/** — Branding and demo assets.

## Prerequisites

- Node.js 18+ and Python 3.10+
- PostgreSQL
- An LLM provider reachable via an OpenAI-compatible endpoint (this deployment routes through 9Router to a vision-capable model)

## Setup

### Backend
```
cd backend
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
copy .env.example .env   # then fill in DB + LLM API key
.venv\Scripts\alembic upgrade head
.venv\Scripts\uvicorn main:app --host 0.0.0.0 --port 8000
```

### Desktop app
```
cd desktop
npm install
cd neuralagent-app && npm install && cd ..
# create the Python venv the Electron app spawns the agent from:
python -m venv aiagent\venv
aiagent\venv\Scripts\pip install -r aiagent\requirements.txt
npm run dev
```

## Configuration

Both `backend/.env` and `desktop/neuralagent-app/.env` must be created from their `.env.example` files. The LLM model IDs and API key live in `backend/.env`. The computer-use agent requires a **vision-capable** model, since it reasons over screenshots of the desktop.

## Note on secrets

API keys and `.env` files are intentionally excluded from this repository. You must supply your own.
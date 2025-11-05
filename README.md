# ChatApp (Django + Channels + React)

A real-time 1:1 chat application with JWT auth, REST APIs, and WebSocket messaging.

- Backend: Django 5, Django REST Framework, Channels (WebSockets), channels-redis, Simple JWT, CORS Headers
- Frontend: React (Vite)
- Realtime transport: Redis-backed channel layer

## Features
- **JWT Authentication** (login, refresh)
- **User management** (register, list users)
- **Conversations** (create between two users, list)
- **Messages** (list, create, delete own)
- **Realtime chat** over WebSockets with typing indicator and online presence

## Project Structure
- **chatapppoj/** Django project root
  - `manage.py`
  - `chatapppoj/` project settings, ASGI, routing
  - `chatapp/` Django app (models, serializers, views, consumers, urls, routing)
  - `db.sqlite3` (development database; do not commit)
- **frontend/** React app (Vite)
  - `src/` components, pages, auth and API helpers
  - `.env` for `VITE_API_URL`

## Backend Overview
- REST endpoints are under `chat/` prefix (see `chatapppoj/chatapppoj/urls.py`).
- Auth: `rest_framework_simplejwt` with access/refresh tokens.
- WebSocket endpoint (see `chatapp/routing.py`):
  - `ws://<HOST>:<PORT>/ws/chat/<conversation_id>/?token=<JWT_ACCESS_TOKEN>`
  - Token is verified in `ChatConsumer.connect`.
- Channel layer: Redis at `127.0.0.1:6379` (see `settings.py`).

### Key Endpoints
- `POST /chat/auth/register/` — create user
- `POST /chat/auth/token/` — obtain JWT (username, password)
- `POST /chat/auth/token/refresh/` — refresh access token
- `GET /chat/users/` — list users (auth required)
- `GET|POST /chat/conversations/` — list or create conversation (exactly two participants incl. self)
- `GET|POST /chat/conversations/<id>/messages/` — list or create message in a conversation
- `GET|DELETE /chat/conversations/<id>/messages/<pk>/` — retrieve or delete message (only sender can delete)

## Frontend Overview
- `src/api.js` injects `Authorization: Bearer <access>` and uses `VITE_API_URL` (default http://127.0.0.1:8000).
- `src/auth.js` manages token refresh and logout.
- `src/components/Conversation.jsx` opens a WebSocket to the backend and handles:
  - `chat_message` — append new message
  - `typing` — show typing indicator
  - `online_status` — track presence in the conversation room

## Requirements
- Python 3.10+ (recommended)
- Node.js 18+
- Redis server (local) for channels layer

## Setup (Development)

### 1) Backend
```bash
# from repository root
python -m venv .venv
.venv\Scripts\activate  # Windows PowerShell: .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Create DB and tables
python chatapppoj/manage.py migrate

# Create a superuser (optional)
python chatapppoj/manage.py createsuperuser

# Start Redis (ensure it runs on 127.0.0.1:6379)
# Windows users: run Redis via Docker or a local install

# Run the ASGI server (recommended for websockets)
python -m daphne -p 8000 chatapppoj.chatapppoj.asgi:application
# Alternatively, for basic dev you can try
python chatapppoj/manage.py runserver  # may not handle websockets fully without Daphne
```

### 2) Frontend
```bash
# from repository root
cd frontend
npm install
# optionally configure API base URL
# echo VITE_API_URL=http://127.0.0.1:8000 > .env
npm run dev
```

Open http://localhost:5173

## Environment Configuration
- Backend `SECRET_KEY` is currently hardcoded in settings for demo purposes. For production, load it from environment variables and disable `DEBUG`.
- Frontend expects `VITE_API_URL` in `frontend/.env` (optional; defaults to http://127.0.0.1:8000).

## Production Notes
- Use a managed Redis instance for channels layer.
- Serve ASGI via Daphne/Uvicorn behind a reverse proxy.
- Configure CORS and allowed hosts.
- Use a production-ready database (PostgreSQL, MySQL) instead of SQLite.

## License
MIT (or your preferred license)

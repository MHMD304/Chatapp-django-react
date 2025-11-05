# 🗨️ ChatApp (Django + Channels + React)

A **real-time 1-to-1 chat application** built with **Django**, **Django REST Framework**, **Channels (WebSockets)**, and **React (Vite)** — featuring **JWT authentication**, REST APIs, and **Redis-backed real-time messaging**.

---

## 🚀 Tech Stack

**Backend**
- Django 5  
- Django REST Framework  
- Django Channels (WebSockets)  
- Channels-Redis  
- Simple JWT  
- Django CORS Headers  

**Frontend**
- React (Vite)  
- Axios  

**Realtime Transport**
- Redis (Channel Layer)

---

## ✨ Features
- 🔐 JWT Authentication (login, refresh)
- 👤 User Management (register, list users)
- 💬 Conversations (create, list)
- 📩 Messages (send, list, delete own)
- ⚡ Real-time WebSocket Chat (typing indicator & online status)
- 🧠 Token-based access validation for WebSocket connections

---

## 📁 Project Structure
```
ChatApp/
│
├── chatapppoj/ # Django project root
│ ├── chatapppoj/ # Project settings, ASGI, routing
│ ├── chatapp/ # Core Django app (models, serializers, consumers, etc.)
│ └── manage.py
│
├── frontend/ # React (Vite) frontend
│ ├── src/ # Components, pages, API & auth helpers
│ └── .env # API base URL (VITE_API_URL)
│
├── requirements.txt # Python dependencies
├── README.md
└── .gitignore
```

## ⚙️ Backend Overview
**Main Endpoints** (prefix: `/chat/`)
| Method | Endpoint | Description |
|:-------|:----------|:-------------|
| POST | `/auth/register/` | Register a new user |
| POST | `/auth/token/` | Obtain JWT access & refresh tokens |
| POST | `/auth/token/refresh/` | Refresh access token |
| GET | `/users/` | List all users (auth required) |
| GET / POST | `/conversations/` | List or create a conversation (two participants) |
| GET / POST | `/conversations/<id>/messages/` | List or send messages in a conversation |
| DELETE | `/conversations/<id>/messages/<pk>/` | Delete your own message |

**WebSocket Endpoint**
ws://<HOST>:<PORT>/ws/chat/<conversation_id>/?token=<JWT_ACCESS_TOKEN>
Token is validated inside `ChatConsumer.connect`.

**Channel Layer:** Redis (`127.0.0.1:6379`)

---

## 🧩 Frontend Overview

- `src/api.js` → Handles REST API requests with `Authorization: Bearer <access>` header.  
- `src/auth.js` → Manages JWT token storage, refresh, and logout.  
- `src/components/Conversation.jsx` → Manages WebSocket connection and handles:
  - `chat_message` → Append new message
  - `typing` → Display typing indicator
  - `online_status` → Track online presence

---

## 🧱 Requirements

- Python 3.10+  
- Node.js 18+  
- Redis (local instance for channel layer)

---

## 🧑‍💻 Setup (Development)
### 1️⃣ Backend
```bash
# From repository root
python -m venv .venv
.venv\Scripts\activate     # PowerShell: .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Create database and apply migrations
python chatapppoj/manage.py migrate

# (Optional) Create an admin user
python chatapppoj/manage.py createsuperuser

# Ensure Redis is running locally (127.0.0.1:6379)

# Run ASGI server (required for WebSockets)
python -m daphne -p 8000 chatapppoj.chatapppoj.asgi:application
# Alternatively:
python chatapppoj/manage.py runserver
### 2️⃣ frontend
cd frontend
npm install

# Optionally set your backend API URL
# echo VITE_API_URL=http://127.0.0.1:8000 > .env

npm run dev
```
## 🧑‍💻 Setup (Development)

Backend SECRET_KEY is currently hardcoded (for demo).
→ In production, load from environment variables and disable DEBUG.

Frontend expects VITE_API_URL inside frontend/.env
→ Defaults to http://127.0.0.1:8000 if not set.

## 🚀 Production Notes

Use a managed Redis instance for the Channels layer.

Serve ASGI using Daphne or Uvicorn behind Nginx or another reverse proxy.

Configure ALLOWED_HOSTS, CORS_ORIGIN_WHITELIST, and secure settings.

Replace SQLite with PostgreSQL or MySQL.

## 📄 License

MIT License — feel free to use and modify for personal or educational projects.

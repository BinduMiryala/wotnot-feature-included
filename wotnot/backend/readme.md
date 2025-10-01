# Backend Setup Instructions

This backend is powered by **FastAPI** and uses **Uvicorn** as the ASGI server. We also use **Dramatiq** for task processing.

---

## 🔧 Setup Instructions

## make sure you use python 3.12.3
### 1. Create and Activate a Virtual Environment

Open your terminal and navigate to the `backend/` folder:

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

---

### 2. Install Dependencies

Install the required packages using `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

## 🚀 Running the Backend Server

To start the FastAPI server with **Uvicorn**:

```bash
uvicorn wati.main:app --reload --port 8000
```

- `--reload` enables hot-reloading during development.
- The server will be available at: `http://localhost:8000`

---

## 🧵 Running the Dramatiq Worker

## pip install dramatiq
Open a **new terminal window**, and make sure to activate the same virtual environment:

```bash
cd backend
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

Then run the Dramatiq worker:

```bash
dramatiq wati.services.tasks
```

This command will start the worker that processes background tasks defined in `wati/services/tasks.py`.

---

## 📁 Project Structure Overview

```
backend/
│
├── venv/                   # Virtual environment
├── wati/
│   ├── main.py             # FastAPI app entry point
│   └── services/
│       └── tasks.py        # Dramatiq tasks
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

---

## ✅ Notes

- Ensure **Redis** is running (required for Dramatiq).
- Use `.env` or environment variables for sensitive configuration (e.g., DB URLs, Redis URI).

---

Happy hacking! 🚀

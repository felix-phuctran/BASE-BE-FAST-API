# FastAPI Base Project

## 📚 Introduction

This is a basic project using **FastAPI**, integrated with **Midgrade** and **CLI** to support system management tasks.

## 📚 Project Structure

```
.vscode/             # VSCode configuration
alembic/             # Database migration management
api/                 # API routes
cli/                 # CLI commands for project management
constants/           # Constants
container/           # Dependency injection management
core/                # System configuration
...
services/            # Business logic processing
utils/               # Helper utilities
main.py              # Main application entry point
requirements.txt     # Required libraries list
Dockerfile           # Docker configuration
```

## 🛠️ Installation

### 1. ✨ Clone Project

```bash
git clone <repository-url>
cd <project-folder>
```

### 2. ⚙️ Create and Activate Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate     # On Windows
```

### 3. 💪 Install Required Libraries

```bash
pip install -r requirements.txt
```

## 🏢 Running the Application

### 1. 🌐 Run FastAPI Server

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Open browser and access:

- API Docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- OpenAPI JSON: [http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json)

### 2. 🛠️ Run CLI

The project supports CLI commands for system management.

Example:

```bash
cd cli/seed_data
python initialize_database.py
```

### 3. 📂 Run Database Migration

```bash
alembic upgrade head
```

## 🛠️ Run with Docker

### 1. 🛠️ Build Image

```bash
docker build -t fastapi-app .
```

### 2. 💨 Run Container

```bash
docker run -p 8000:8000 fastapi-app
```

## 📝 Notes

- Ensure **Python 3.9+**
- Update `.env` according to environment configuration before running

## 📢 Contact

If you encounter any issues, please contact the development team for support! 🌟

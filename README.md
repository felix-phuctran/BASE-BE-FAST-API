# FastAPI Base Project

## Giới thiệu

Đây là dự án cơ bản sử dụng **FastAPI**, có tích hợp **Midgrade** và **CLI** để hỗ trợ các tác vụ quản lý hệ thống.

## Cấu trúc dự án

```
.vscode/
alembic/             # Quản lý migration database
api/                 # Các route API
cli/                 # Lệnh CLI để quản lý dự án
constants/           # Chứa các hằng số
container/           # Quản lý dependency injection
core/                # Cấu hình hệ thống
...
services/            # Xử lý logic nghiệp vụ
utils/               # Các tiện ích hỗ trợ
main.py              # Điểm khởi chạy chính của ứng dụng
requirements.txt     # Danh sách thư viện cần thiết
Dockerfile           # Cấu hình Docker
```

## Cài đặt

### 1. Clone dự án

```bash
git clone <repository-url>
cd <project-folder>
```

### 2. Tạo và kích hoạt môi trường ảo

```bash
python -m venv venv
source venv/bin/activate  # Trên macOS/Linux
venv\Scripts\activate     # Trên Windows
```

### 3. Cài đặt các thư viện cần thiết

```bash
pip install -r requirements.txt
```

## Chạy ứng dụng

### 1. Chạy server FastAPI

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Mở trình duyệt và truy cập:

- API Docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- OpenAPI JSON: [http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json)

### 2. Chạy CLI

Dự án có hỗ trợ các lệnh CLI để quản lý hệ thống.

Ví dụ:

```bash
cd cli/seed_data
python initialize_database.py
```

### 3. Chạy migration database

```bash
alembic upgrade head
```

## Chạy với Docker

### 1. Build image

```bash
docker build -t fastapi-app .
```

### 2. Chạy container

```bash
docker run -p 8000:8000 fastapi-app
```

## Ghi chú

- Đảm bảo có **Python 3.9+**
- Cập nhật `.env` theo cấu hình môi trường của bạn trước khi chạy

## Liên hệ

Nếu có bất kỳ vấn đề gì, hãy liên hệ nhóm phát triển để được hỗ trợ.

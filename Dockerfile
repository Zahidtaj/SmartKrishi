# Stage 1: Build React + TypeScript + Vite frontend
FROM node:22-slim AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

# Stage 2: FastAPI + ML + SQLite production runtime
FROM python:3.13-slim
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
WORKDIR /app

COPY backend/requirements.txt ./backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt

COPY backend/ ./backend/
COPY ml/ ./ml/
COPY datasets/ ./datasets/
COPY pytest.ini ./pytest.ini
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

RUN python -m ml.train && python -m backend.seed

EXPOSE 8000
CMD ["sh", "-c", "uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-8000}"]

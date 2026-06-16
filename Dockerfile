# Stage 1: Build frontend
FROM node:22-alpine AS frontend-builder
WORKDIR /app/frontend
COPY x10-frontend/package.json ./
RUN npm install
COPY x10-frontend/ .
RUN npm run build:docker

# Stage 2: Production image
FROM python:3.11-slim
WORKDIR /app

# Install backend dependencies
COPY x10-backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY x10-backend/ .

# Copy built frontend
COPY --from=frontend-builder /app/frontend/dist ./static

# CloudBase 云托管使用 $PORT 环境变量传递端口
CMD sh -c "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080}"

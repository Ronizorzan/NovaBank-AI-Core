# === Estágio 1: Builder (Compilação) ===
FROM python:3.12-slim AS builder
WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN pip install uv && uv pip install . --system

# === Estágio 2: Runtime (Imagem Final Leve) ===
FROM python:3.12-slim
WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV ENV=production

# Copiar dependências do builder
COPY --from=builder /usr/local /usr/local

# Copiar código fonte
COPY . .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]

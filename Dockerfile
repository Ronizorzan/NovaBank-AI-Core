# Dockerfile moderno e otimizado usando o 'uv' para FastAPI RAG
# Estágio 1: Build (Gerar o ambiente de dependências)
FROM python:3.11-slim as BUILDER
WORKDIR /app

# Instalar o gerenciador de pacotes 'uv' no container
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv


# Copiar os arquivos de definição de pacotes e lock
COPY pyproject.toml uv.lock README.md ./

# Sincronizar as dependências e criar um ambiente virtual em /app/.venv
# Usamos '--no-dev' para excluir pacotes de desenvolvimento (como pytest)
RUN uv sync --frozen --no-dev --no-install-project

# Estágio 2: Final/Runtime (Imagem de execução leve)
FROM python:3.11-slim
WORKDIR /app

# Variável de ambiente essencial para garantir logs em tempo real
ENV PYTHONUNBUFFERED=1

# Variável de ambiente para que as LLMs/provedores saibam que estão em produção
ENV ENV=production

# Copiar o ambiente virtual já populado do estágio builder
COPY --from=builder /app/.venv /app/.venv

# Copiar todo o código fonte e as pastas de dados
# chroma_db_faq, files (contendo PDFs), data, functions_src
COPY . .

# Atualizar o PATH para usar o ambiente virtual por padrão
ENV PATH="/app/.venv/bin:$PATH"

# Definir a variável de porta que a nuvem usa
# O FastAPI padrão é 8000, mas a nuvem costuma ouvir em 80 ou 443 
# e redirecionar para a porta que definirmos aqui.
EXPOSE 8000

# Comando de inicialização usando uvicorn.
# É CRÍTICO manter '--host 0.0.0.0' para acesso externo.
# '--proxy-headers' é boa prática para obter o IP correto do cliente atrás de balanceadores da nuvem.
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers", "--forwarded-allow-ips='*'"]
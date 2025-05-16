FROM python:3.10-slim

WORKDIR /app

# Copiar arquivos
COPY . /app/

# Instalar dependências do diretório app (ajuste conforme necessário)
RUN pip install --no-cache-dir -r app/requirements.txt

EXPOSE 8001

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
FROM python:3.10-slim

WORKDIR /app

# Copia o arquivo de requisitos e instala as dependências
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante dos arquivos da aplicação
WORKDIR /app

COPY server.py ./

CMD ["python", "server.py"]

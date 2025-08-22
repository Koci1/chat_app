# Dockerfile
FROM --platform=linux/amd64 python:3.12-slim

WORKDIR /app

# Kopiraj requirements i instaliraj
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Kopiraj ostatak projekta
COPY . .

# CMD za Daphne (provjeri path do ASGI)
CMD ["python", "-m", "daphne", "-b", "0.0.0.0", "-p", "8000", "chat_app.asgi:application"]
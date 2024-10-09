FROM debian:bookworm-slim

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    libreoffice \
    && apt-get clean

WORKDIR /app

COPY requirements.txt ./

COPY app.py .

RUN python3 -m venv venv

RUN ./venv/bin/pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["./venv/bin/python", "app.py"]

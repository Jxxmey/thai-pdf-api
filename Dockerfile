FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    python3-cffi \
    python3-brotli \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libharfbuzz-subset0 \
    libjpeg-dev \
    libopenjp2-7-dev \
    libcairo2 \
    curl \
    fontconfig \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /usr/share/fonts/truetype/google-fonts
RUN curl -L https://github.com/google/fonts/raw/main/ofl/sarabun/Sarabun-Regular.ttf -o /usr/share/fonts/truetype/google-fonts/Sarabun-Regular.ttf
RUN curl -L https://github.com/google/fonts/raw/main/ofl/sarabun/Sarabun-Bold.ttf -o /usr/share/fonts/truetype/google-fonts/Sarabun-Bold.ttf
RUN fc-cache -f -v

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 80
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
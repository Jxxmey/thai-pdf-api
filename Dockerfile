# ใช้ Python 3.10 ตัวเล็ก (Slim)
FROM python:3.10-slim

# ตั้งค่าไม่ให้ Python สร้าง .pyc file
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 1. ติดตั้ง Library ของระบบที่ WeasyPrint ต้องการ (Pango, Cairo)
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

# 2. ติดตั้ง Font ภาษาไทย (Sarabun) จาก Google Fonts
RUN mkdir -p /usr/share/fonts/truetype/google-fonts
RUN curl -L https://github.com/google/fonts/raw/main/ofl/sarabun/Sarabun-Regular.ttf -o /usr/share/fonts/truetype/google-fonts/Sarabun-Regular.ttf
RUN curl -L https://github.com/google/fonts/raw/main/ofl/sarabun/Sarabun-Bold.ttf -o /usr/share/fonts/truetype/google-fonts/Sarabun-Bold.ttf

# สั่ง Refresh Cache ของ Font
RUN fc-cache -f -v

# 3. เตรียมโฟลเดอร์งาน
WORKDIR /app

# 4. ติดตั้ง Python Libraries
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. คัดลอกโค้ด
COPY . .

# 6. เปิด Port และรัน
EXPOSE 8000
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
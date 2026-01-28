FROM python:3.9-slim

# 1. Cài đặt toàn bộ công cụ biên dịch và thư viện hệ thống
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    pkg-config \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libavdevice-dev \
    libavfilter-dev \
    libavformat-dev \
    libavcodec-dev \
    libswresample-dev \
    libswscale-dev \
    libavutil-dev \
    && rm -rf /var/lib/apt/lists/*

# 2. Cấu hình User
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH
WORKDIR $HOME/app

# 3. Cài đặt Python dependencies
COPY --chown=user:user requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 4. Copy mã nguồn
COPY --chown=user:user . .

# 5. Khởi chạy
CMD ["streamlit", "run", "app.py", "--server.port=7860", "--server.address=0.0.0.0"]
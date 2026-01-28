# Sử dụng Python slim image
FROM python:3.9-slim

# Cài đặt các thư viện hệ thống (Đã sửa đổi cho Debian Trixie/Bookworm)
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Các phần còn lại giữ nguyên
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app

COPY --chown=user:user requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=user:user . .

CMD ["streamlit", "run", "app.py", "--server.port=7860", "--server.address=0.0.0.0"]
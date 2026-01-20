FROM python:3.11-slim

# ---- system deps ----
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# ---- python deps ----
# 先裝 uv
RUN pip install --no-cache-dir uv

# 明確裝 CPU-only torch（關鍵）
RUN pip install --no-cache-dir \
    torch torchvision torchaudio \
    --index-url https://download.pytorch.org/whl/cpu

# 再裝你自己的 dependencies（ultralytics 就不會拉 CUDA 了）
COPY pyproject.toml uv.lock* ./
RUN uv pip install --system .

# ---- app code ----
COPY app ./app
COPY static ./static

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

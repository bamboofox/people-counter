FROM python:3.11-slim

# ---- system deps ----
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# ---- workdir ----
WORKDIR /app

# ---- python deps ----
COPY pyproject.toml uv.lock* ./
RUN pip install --no-cache-dir uv \
 && uv pip install --system .

# ---- app code ----
COPY app ./app
COPY static ./static

# ---- runtime ----
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

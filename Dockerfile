FROM python:3.11-slim-bookworm

# Set environment for deterministic Python behavior
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8000

WORKDIR /app

# Install Python dependencies first (cache layer)
COPY requirements.txt .
# Upgrade pip and install from requirements.txt without cache to keep image smaller
RUN python -m pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user and give ownership of application files
RUN groupadd --gid 1000 app && useradd --uid 1000 --gid app --shell /bin/sh --create-home app \
    && chown -R app:app /app

USER app

# Expose application port and run uvicorn binding to 0.0.0.0
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]

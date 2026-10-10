FROM python:3.12-slim-bookworm

# Use a non-root user
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    PATH="/home/app/.local/bin:${PATH}"

# Create app user and directory
RUN useradd --create-home --home-dir /home/app --shell /bin/bash app
WORKDIR /app

# Install pip requirements deterministically
COPY requirements.txt .
# Upgrade core packaging tools then install requirements.
# Keep installation minimal; many wheels are available for pinned versions.
RUN python -m pip install --upgrade pip setuptools wheel \
 && python -m pip install --no-cache-dir -r requirements.txt \
 && rm -rf /root/.cache/pip

# Copy application code
COPY . /app
RUN chown -R app:app /app

# Switch to non-root user
USER app

# Expose default FastAPI/uvicorn port
EXPOSE 8000

# Run the app with uvicorn, binding to 0.0.0.0
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--loop", "auto", "--http", "auto"]

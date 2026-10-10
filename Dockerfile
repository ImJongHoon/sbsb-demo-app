FROM python:3.12-slim-bookworm

# Create a non-root user and group
ENV APP_HOME=/app \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VIRTUALENVS_CREATE=false

RUN groupadd --gid 1000 app \
 && useradd --uid 1000 --gid app --home-dir ${APP_HOME} --create-home --shell /bin/false app

WORKDIR ${APP_HOME}

# Install Python dependencies deterministically
# Copy only requirements first to leverage Docker layer caching
COPY requirements.txt .

# Use pip to install exact/locked deps from requirements.txt
RUN python -m pip install --upgrade pip setuptools \
 && pip install --no-cache-dir --requirement requirements.txt

# Copy application code
COPY . .

# Ensure app files are owned by non-root user
RUN chown -R app:app ${APP_HOME}

# Switch to non-root user
USER app

# Expose the port used by uvicorn
EXPOSE 8000

# Run the application; bind to 0.0.0.0 for container networking
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--loop", "auto", "--workers", "1"]

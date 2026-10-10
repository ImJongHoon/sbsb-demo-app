FROM python:3.12-slim-bookworm

# Create a non-root user and app directory
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    APP_HOME=/app

RUN addgroup --system appgroup && adduser --system --ingroup appgroup --home ${APP_HOME} appuser

WORKDIR ${APP_HOME}

# Install Python dependencies deterministically from requirements.txt
# --prefer-binary helps avoid building from source when wheels are available.
# Do not install OS build tools; requirements are expected to provide binary wheels.
COPY requirements.txt .
RUN pip install --no-cache-dir --disable-pip-version-check --prefer-binary -r requirements.txt

# Copy application code and ensure correct ownership
COPY --chown=appuser:appgroup . .

# Use non-root user
USER appuser

# Expose the port the app serves on and run Uvicorn binding to 0.0.0.0
EXPOSE 8000

# Runtime command: single worker Uvicorn suitable for containerized deployments.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--limit-concurrency", "100"]

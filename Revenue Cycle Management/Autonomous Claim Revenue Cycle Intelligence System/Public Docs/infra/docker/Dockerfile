FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ src/
COPY pyproject.toml .
RUN pip install --no-cache-dir -e .

# TODO(architect): add non-root user, healthcheck, and proper entrypoint
# once the orchestrator API service is implemented.
CMD ["python", "-m", "denialiq_engine"]

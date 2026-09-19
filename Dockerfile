FROM python:3.12.11-slim AS builder
WORKDIR /app
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip==25.2 && pip install --no-cache-dir -r requirements.txt

FROM python:3.12.11-slim AS runtime
WORKDIR /app
RUN groupadd --system appgroup && useradd --system --gid  appgroup --create-home --home-dir /home/appuser appuser
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY --chown=appuser:appgroup app ./app
EXPOSE 8000
USER appuser
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

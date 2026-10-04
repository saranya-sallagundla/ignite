# Stage 1: builder
FROM python:3.12-slim AS builder
WORKDIR /app
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: final
FROM python:3.12-slim
WORKDIR /app
RUN useradd --create-home appuser
COPY --from=builder --chown=appuser /opt/venv /opt/venv
COPY --chown=appuser app.py .
ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1
USER appuser
EXPOSE 5000
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')"
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]

# Multi-stage: build dependencies in one layer, run in slim layer
FROM python:3.11-slim as runtime

# system deps
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        tini && \
    rm -rf /var/lib/apt/lists/*

# create non-root user
RUN useradd -m -u 1000 appuser
WORKDIR /app
USER appuser

# copy only what we need
COPY --chown=appuser:appuser requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=appuser:appuser src/ ./src/
COPY --chown=appuser:appuser scripts/ ./scripts/
COPY --chown=appuser:appuser tests/ ./tests/

# default command
ENTRYPOINT ["tini", "--"]
CMD ["python", "-m", "src.app"]
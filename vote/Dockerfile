FROM python:3.13-slim-bookworm AS base
WORKDIR /usr/local/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN useradd --create-home --uid 10001 appuser
ENV PORT=8080
EXPOSE 8080

FROM base AS dev
COPY --chown=appuser:appuser . .
USER appuser
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8080", "--reload", "--access-logfile", "-"]

FROM base AS final
COPY --chown=appuser:appuser . .
USER appuser
HEALTHCHECK --interval=15s --timeout=5s --start-period=10s CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8080/', timeout=3)"]
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8080", "--workers", "4", "--access-logfile", "-", "--error-logfile", "-"]

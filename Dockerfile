FROM python:3.11-slim AS base
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1

FROM base AS builder
RUN pip install --upgrade pip build
COPY . .
RUN pip install -e .

FROM base AS production
RUN groupadd --gid 1001 appgroup \
 && useradd --uid 1001 --gid appgroup --no-create-home appuser
COPY --from=builder /app /app
COPY --from=builder /usr/local/lib/python3.11 /usr/local/lib/python3.11
COPY --from=builder /usr/local/bin /usr/local/bin
USER appuser
ENTRYPOINT ["fastenv"]
CMD ["--help"]

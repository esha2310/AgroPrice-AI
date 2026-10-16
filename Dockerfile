FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 DEBUG=0
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN DEBUG=1 python manage.py collectstatic --noinput
RUN useradd --create-home agro && mkdir -p /var/lib/agroprice && chown agro:agro /var/lib/agroprice
ENV DATA_DIR=/var/lib/agroprice
USER agro
EXPOSE 8000
CMD ["sh", "-c", "python manage.py migrate --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 2 --timeout 60"]

FROM python:alpine

ENV FLASK_ENV=production
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app/

CMD ["gunicorn","--workers", "1","--bind","0.0.0.0:5000","wsgi:app","--max-requests","10000","--timeout", "5","--keep-alive","5","--log-level","info"]

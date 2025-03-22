FROM python:3.12-slim

WORKDIR /app

ENV FLASK_APP=main.py
ENV FLASK_ENV=production
ENV PORT=7860

RUN apt-get update && apt-get install -y \
    libopencv-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 7860

CMD ["python","-m","gevent.pywsgi","-b","0.0.0.0:7860","main:app"]
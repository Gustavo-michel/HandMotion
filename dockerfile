FROM python:3.11-slim
 
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

ENV DISPLAY=:99

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["xvfb-run", "gunicorn", "--bind", "0.0.0.0:5000", "--threads", "--log-level", "debug" "4", "app:app"]

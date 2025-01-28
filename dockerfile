FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    libgl1 \
    xorg \
    xvfb \
    && apt-get clean

WORKDIR /app

COPY . /app

ENV DISPLAY=:1

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["Xvfb", ":1", "-screen", "0", "1024x768x16", "&", "gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
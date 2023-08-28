FROM python:3.10
WORKDIR /app
COPY requirements.txt .

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install --no-cache-dir -r requirements.txt

ENV DJANGO_SETTINGS_MODULE celery_test.settings

COPY . .



# docker-compose up --build
# docker ps -> id's
# docker logs
# docker exec -it <id> sh
FROM python:3.8-alpine
RUN apk add  --no-cache ffmpeg

COPY . /app

WORKDIR /app

RUN pip install -r bot_requirements.txt

CMD python ./main.py
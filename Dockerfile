FROM python:3.7-alpine
WORKDIR /code
RUN apk add --no-cache gcc musl-dev linux-headers libc6-compat libstdc++
COPY . .
RUN pip install -r requirements.txt
CMD ["gunicorn","--bind","0.0.0.0:8080","--log-file","error.log","app:app"]

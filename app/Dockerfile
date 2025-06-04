FROM python:3.13-alpine

WORKDIR /app

RUN apk update && \
    apk add --no-cache build-base

COPY . .

RUN make deps

RUN make dbpush

EXPOSE 8000

CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]
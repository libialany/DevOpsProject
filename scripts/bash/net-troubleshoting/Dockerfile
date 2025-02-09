FROM alpine:latest

RUN apk add --no-cache bash iputils

WORKDIR /app

COPY main.sh .

RUN chmod +x main.sh

ENTRYPOINT ["./main.sh"]
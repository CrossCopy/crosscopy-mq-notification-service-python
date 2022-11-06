# CrossCopy Message Queue Notification System

## Build Docker Image

Here is just a sample, you may need to change the docker registry, image name and tag, network name, etc, depending how how they are defined in your environment.

```bash
docker build . -t ghcr.io/crosscopy/xc-mq-notification:latest
docker run --rm -it --env-file ./.env --network=crosscopy ghcr.io/crosscopy/xc-mq-notification:latest
docker push ghcr.io/crosscopy/xc-mq-notification:latest
```

## Environment Variables

Create a `.env` file with the following template

```
EMAIL_ADDRESS=noreply@gmail.com
EMAIL_PASSWORD=password
MAIL_SERVER=smtp.gmail.com
KAFKA_MODE=local
KAFKA_BOOTSTRAP_SERVERS=kafka:9092
KAFKA_SECURITY_PROTOCOL=
KAFKA_SASL_MECHANISMS=
KAFKA_SASL_USERNAME=
KAFKA_SASL_PASSWORD=
```

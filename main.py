import os
import sys
from confluent_kafka import Consumer, KafkaError, KafkaException, admin

from src.constant import topics
from src.handler import signup_handler

KAFKA_MODE = os.environ.get("KAFKA_MODE")
KAFKA_BOOTSTRAP_SERVERS = os.environ.get("KAFKA_BOOTSTRAP_SERVERS")
KAFKA_SECURITY_PROTOCOL = os.environ.get("KAFKA_SECURITY_PROTOCOL")
KAFKA_SASL_MECHANISMS = os.environ.get("KAFKA_SASL_MECHANISMS")
KAFKA_SASL_USERNAME = os.environ.get("KAFKA_SASL_USERNAME")
KAFKA_SASL_PASSWORD = os.environ.get("KAFKA_SASL_PASSWORD")
print(f"KAFKA_MODE: {KAFKA_MODE}")
print(f"KAFKA_BOOTSTRAP_SERVERS: {KAFKA_BOOTSTRAP_SERVERS}")
print(f"KAFKA_SECURITY_PROTOCOL: {KAFKA_SECURITY_PROTOCOL}")
print(f"KAFKA_SASL_MECHANISMS: {KAFKA_SASL_MECHANISMS}")
print(f"KAFKA_SASL_USERNAME: {KAFKA_SASL_USERNAME}")
print(f"KAFKA_SASL_PASSWORD: {KAFKA_SASL_PASSWORD}")
running = True
MIN_COMMIT_COUNT = 1


def commit_completed(err, partitions):
    if err:
        print(str(err))
    else:
        print("Committed partition offsets: " + str(partitions))


conf = {
    'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
    'session.timeout.ms': '45000'
}

if KAFKA_MODE == 'cloud':
  conf['sasl.username'] = KAFKA_SASL_USERNAME
  conf['sasl.password'] = KAFKA_SASL_PASSWORD
  conf['security.protocol'] = KAFKA_SECURITY_PROTOCOL
  conf['sasl.mechanisms'] = KAFKA_SASL_MECHANISMS

adminClient = admin.AdminClient(conf)
# ? https://docs.confluent.io/platform/current/clients/confluent-kafka-python/html/index.html#newtopic
new_topics = [admin.NewTopic(topic, 1) for topic in topics.TOPICS]
print(f"Create Topics: {str(topics.TOPICS)}")
adminClient.create_topics(new_topics)
conf.update({
    'group.id': "crosscopy-notification",
    'default.topic.config': {'auto.offset.reset': 'smallest'},
    'on_commit': commit_completed
})
consumer = Consumer(conf)


def msg_process(msg):
    topic = msg.topic()
    if topic == topics.SIGNUP:
        signup_handler(msg)


def consume_loop(consumer, topics):
    try:
        consumer.subscribe(topics)
        msg_count = 0
        while running:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                                     (msg.topic(), msg.partition(), msg.offset()))
                elif msg.error():
                    raise KafkaException(msg.error())
            else:
                msg_process(msg)
                msg_count += 1
                if msg_count % MIN_COMMIT_COUNT == 0:
                    consumer.commit(asynchronous=True)
    finally:
        # Close down consumer to commit final offsets.
        consumer.close()


def shutdown():
    running = False


if __name__ == "__main__":
    print("Notification Consumer Started")
    consume_loop(consumer, [topics.SIGNUP])

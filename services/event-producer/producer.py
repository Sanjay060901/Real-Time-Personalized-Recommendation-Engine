# services/event-producer/producer.py
import json
import time
import random
from kafka import KafkaProducer


KAFKA_BOOTSTRAP = 'kafka:9092'
TOPIC = 'events'


producer = KafkaProducer(
bootstrap_servers=[KAFKA_BOOTSTRAP],
value_serializer=lambda v: json.dumps(v).encode('utf-8')
)


PRODUCTS = [
{"id": "p1", "category": "shoes"},
{"id": "p2", "category": "socks"},
{"id": "p3", "category": "tshirt"},
{"id": "p4", "category": "watch"},
]


USERS = ["u1","u2","u3","u4","u5"]


EVENT_TYPES = ["view","click","add_to_cart","purchase"]




def gen_event():
user = random.choice(USERS)
prod = random.choice(PRODUCTS)
event = {
"user_id": user,
"product_id": prod['id'],
"category": prod['category'],
"event_type": random.choices(EVENT_TYPES, weights=[0.6,0.25,0.1,0.05])[0],
"timestamp": int(time.time() * 1000)
}
return event




if __name__ == '__main__':
print('Starting event producer...')
while True:
ev = gen_event()
producer.send(TOPIC, ev)
print('sent', ev)
time.sleep(random.random() * 1.5)

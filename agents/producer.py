import itertools
import json
import time

from kafka import KafkaProducer
from kafka.errors import KafkaError

from dublin_data_creation import StoreGenerator as DublinStoreGenerator


producer = KafkaProducer(
     bootstrap_servers=['kafka:9092', 'kafka1:9093', 'kafka2:9094'],
)

data_generator = DublinStoreGenerator()
counter = itertools.count()

# while True:
for i in range(10):
    data = data_generator.generate_data_json()
    future = producer.send('test', json.dumps(data).encode(encoding='utf-8'))

    try:
        record_metadata = future.get(timeout=5)

        # Successful result returns assigned partition and offset
        print("sent msg %d@%d to topic %s"%(record_metadata.offset, record_metadata.partition, record_metadata.topic))

    except KafkaError as ke:
        print(ke)

    # time.sleep(5)

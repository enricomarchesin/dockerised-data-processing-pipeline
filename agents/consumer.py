import json

import pandas as pd
import pytz
from kafka import KafkaConsumer
from sqlalchemy import create_engine


my_timezone = pytz.timezone('Europe/Dublin')
dbengine = create_engine("postgres+psycopg2://postgres:postgres@postgres:5432/postgres")

consumer = KafkaConsumer(
    'test',
     bootstrap_servers=['kafka:9092', 'kafka1:9093', 'kafka2:9094'],
     auto_offset_reset='earliest',
     enable_auto_commit=False,
     group_id='test-consumers',
     value_deserializer=lambda m: m.decode('utf-8'),
)

for topic in consumer.topics():
    print("Subscribed to topic:", topic)
    print("-", "partitions:", consumer.partitions_for_topic(topic))

while True:
    r = consumer.poll(5000)
    for topic, records in r.items():
        print('from topic:', topic.topic)
        for record in records:
            df = pd.read_json(record.value, lines=True)
            print('-', df.head())
            df.to_sql('overall_data', if_exists='append', con=dbengine, index=False)
    consumer.commit()

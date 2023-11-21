import sqlite3
import json
from kafka import KafkaProducer

#Kafka
KAFKA_BROKERS: str = (
    "strimzi-kafka-bootstrap.kafka:9092"  # <service name>.<namepsace>:<port>
)
DEFAULT_TOPIC: str = "SWITRS"
DEFAULT_ENCODING: str = "utf-8"

producer = KafkaProducer(bootstrap_servers=KAFKA_BROKERS)

#Sqlite3
con = sqlite3.connect("/root/switrs.sqlite")
cur = con.cursor()

queryCollisionsTable = (
        "SELECT * FROM collisions"
    )
queryCollisionsCaseID = (
        "SELECT case_id FROM collisions"
    )

#Produces every row within the collision table into the Kafka Cluster.
for result in cur.execute(queryCollisionsTable):
    producer.send(DEFAULT_TOPIC, key=bytes(result[0], DEFAULT_ENCODING), value=bytes(json.dumps(result), DEFAULT_ENCODING))  

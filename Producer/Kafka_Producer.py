import sqlite3
import json
import threading
import pandas as pd
import math
from kafka import KafkaProducer

### KAFKA ###
KAFKA_BROKERS: str = (
    "strimzi-kafka-bootstrap.kafka:9092"  # <service name>.<namepsace>:<port>
)

#acks to force Kafka into commiting to sending the messages and not letting them drop in transition.
producer = KafkaProducer(bootstrap_servers=KAFKA_BROKERS, acks='all', retries=5)

DEFAULT_ENCODING: str = "utf-8"

COORDINATES: str = "COORDINATES"

#SWIRTS TOPICS
SWITRS_COLLISIONS: str = "SWITRS_COLLISIONS"
SWITRS_PARTIES: str = "SWITRS_PARTIES"
SWITRS_VICTIMS: str = "SWITRS_VICTIMS"


### SWIRTS DATASET ###
# QUERIES FOR DATES
queryCollisionsDates = (
        '''SELECT * FROM collisions WHERE process_date >= '2019-01-01';'''
    )
queryVictimsDates = (
        '''SELECT * FROM victims WHERE case_id IN (SELECT case_id FROM collisions WHERE process_date >= '2019-01-01');'''
    )

queryPartiesDates = (
        '''SELECT * FROM parties WHERE case_id IN (SELECT case_id FROM collisions WHERE process_date >= '2019-01-01');'''
    )

### READING FROM SQLITE FILE ###
def kafkaProducer_send(query, topic):
    con = sqlite3.connect("/root/switrs_modified.sqlite", check_same_thread=False)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    columns = cur.execute(query).description
    columnName = columns[0][0]

    for result in cur.execute(query):
        row = dict(result)
        id:str = row[columnName]
        producer.send(topic, key=bytes(str(id), DEFAULT_ENCODING), value=bytes(json.dumps(row), DEFAULT_ENCODING))  

### READING FROM CSV FILE ###
# Using pandas is unnesary for this part but that's a fix for later...Too Bad!
def produce_Coordinates():
    df_cordinates = pd.read_csv("/root/coordinates.csv")

    df_cordinates = df_cordinates.astype(object)
    for index, row in df_cordinates.iterrows():
        result = dict(row)
        
        del result[list(result.keys())[0]]

        result = str(result['case_id'])

        id = result['case_id']

        if math.isnan(result['latitude']):
            result['latitude'] = None
            
        if math.isnan(result['longitude']):
            result['longitude'] = None

        producer.send(COORDINATES, key=bytes(str(id), DEFAULT_ENCODING), value=bytes(json.dumps(row), DEFAULT_ENCODING))

### MULTI THREADING ###
#threading.Thread(target=kafkaProducer_send, args=(queryCollisionsTable, SWITRS_COLLISIONS,)).start()
#threading.Thread(target=kafkaProducer_send, args=(queryPartiesTable, SWITRS_PARTIES,)).start()
#threading.Thread(target=kafkaProducer_send, args=(queryVictimsTable, SWITRS_VICTIMS,)).start()

#threading.Thread(target=produce_Coordinates).start()


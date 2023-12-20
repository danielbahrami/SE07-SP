curl -X POST \
http://127.0.0.1:8083/connectors \
-H 'Content-Type: application/json' \
-d '{
    "name": "mongodb-sink",
    "config": {
        "connection.password": "password",
        "connection.uri": "mongodb://admin:password@mongodb.mongodb:27017",
        "connection.url": "mongodb://mongodb.mongodb:27017",
        "connection.username": "admin",
        "connector.class": "com.mongodb.kafka.connect.MongoSinkConnector",
        "database": "kafka",
        "key.converter": "org.apache.kafka.connect.storage.StringConverter",
        "key.converter.schemas.enable": "true",
        "name": "mongodb-sink",
        "output.format.key": "json",
        "output.format.value": "json",
        "post.processor.chain": "com.mongodb.kafka.connect.sink.processor.DocumentIdAdder",
        "tasks.max": "4",
        "timeseries.timefield.auto.convert": "false",
        "topics": "SWITRS_COLLISIONS_NEW, SWITRS_CASE_IDS,SWITRS_PARTIES,SWITRS_VICTIMS",
        "value.converter": "org.apache.kafka.connect.storage.StringConverter",
        "value.converter.schemas.enable": "true"
    }
}'

curl -X POST \
http://127.0.0.1:8083/connectors \
-H 'Content-Type: application/json' \
-d '{
    "name": "mongodb-sink",
    "config": {
        "connection.password": "password",
        "connection.uri": "mongodb://admin:password@mongodb.mongodb:27017",
        "connection.url": "mongodb://mongodb.mongodb:27017",
        "connection.username": "admin",
        "connector.class": "com.mongodb.kafka.connect.MongoSinkConnector",
        "database": "kafka",
        "key.converter": "org.apache.kafka.connect.storage.StringConverter",
        "key.converter.schemas.enable": "true",
        "name": "mongodb-sink",
        "output.format.key": "json",
        "output.format.value": "json",
        "post.processor.chain": "com.mongodb.kafka.connect.sink.processor.DocumentIdAdder",
        "tasks.max": "4",
        "timeseries.timefield.auto.convert": "false",
        "topics": "COMBINED_SWITRS_COLLISIONS, SWITRS_CASE_IDS,SWITRS_PARTIES,SWITRS_VICTIMS",
        "value.converter": "org.apache.kafka.connect.storage.StringConverter",
        "value.converter.schemas.enable": "true"
    }
}'

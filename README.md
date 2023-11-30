
# SE07-SP

Software Engineering, 7th semester - Semester Project: Scalable Systems

# Currently
We can write to Kafka and store the produced messages within HDFS by using `kafka-connect-sink to HDFS`.

A general diagram of the current system is at: https://drive.google.com/file/d/1ElPVISdFzTpz0xd4Z1crDqeSyA9Lkf_f/view?usp=drive_link
![image](https://github.com/danielbahrami/SE07-SP/assets/55737559/fba6c0d4-bfab-4444-adb4-46bfb5a85c2c)

# Backlog

## Running Spark tasks to group both datasets together

Right now we only have the single dataset, SWITRS, in our system. One of the major points of the project was combining two datasets together, therefore we need Spark for us 

## Setting up our Backend and Frontend

We also need a backend and frontend, the database is ready with the SWIRTS dataset so we can already start feeding it into the backend and then create some Data Visualization.

# Outdated Backlog -23/11/2023-

## Include More Tables from the data set and add the Column's names in the JSON data sent to Kafka Broker - FIXED BY KASIM

As of now the data is taken from the SWITRS.sqlite and the collisions table is queried, then for each row of the local relational database is sent to the Kafka Broker with the key being case_id and the value being a json dump of the row with no meaning and reference to the column. 
This aspect should either be fixed when producing data to the Kafka Broker or it could be prescribed when reading data from HDFS with Spark and then sending the data to MongoDB.
Furthermore, we need to include all of the tables within the data set and perhaps create a topic for each of them inside of Kafka.

### Proposal - Kasim
Using row_factory within the SQLITE3 libary in python for the cursor executions to return dicts instead of tuples, retraining the label and value by using json.dumps(dict(result)).
You will also see in the Ubuntu pod that multi-threading has also been implemented.
```
def kafkaProducer_send(query, topic):
    con = sqlite3.connect("/root/switrs.sqlite", check_same_thread=False)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    columns = cur.execute(query).description
    columnID_name = columns[0][0]
    for result in cur.execute(query):
        row = dict(result)
        id: str = row[columnID_name]
        producer.send(topic, key=bytes(str(id), DEFAULT_ENCODING), value=bytes(json.dumps(dict(result)), DEFAULT_ENCODING))  
```

## Setting up MongoDB and Spark to read data from HDFS - FIXED BY KASIM

Currently, for our production environment at 21/11/2023, we only have STACKABLE, KAFKA, HDFS and UBUNTU pods/services running. As of now one can write data with the Ubuntu VM and it will be sent into Kafka Broker, then through the HDFS 2 Sink Connector the topics are supplied into HDFS.  
Therefore, we need the last steps in reading from the HDFS with Spark and then supplying the data to MongoDB connected to our yet-to-be backend.

### Proposal - Kasim 
Mongodb and kafka connect is alot easier since there is official support. Hdfs and mongodb connector was deprecated in favour of apache Spark. 
Therefore, why not just use kafka instead?

Currently, we now have HDFS sink connector and MongoDB sink connector

# Current Namespaces created

stackable, storage, kafka

# Installation

**I HAVE INSTALLED THE NESSARY COMPNENTS: HDFS, STACKABLE ,KAFKA, UBUNTU PRODUCER. 
*DO NOT* GO INSTALLING THESE WITHIN THE MICROK8S SERVERS. THIS IS SIMPLY A GUIDE IN HOW EVERYTHING HAS BEEN SET UP SO FAR -- 21/11/2023***

## HDFS

First installing the operators needed for HDFS using the Stackable guide and using helm.
When using MicroK8s, the following option is needed when installing with helm `--set kubeletDir=/var/snap/microk8s/common/var/lib/kubelet.
Furthermore, the namespace `stackable` was created for them as they will be deployed at that namespace. 
```
helm install --wait zookeeper-operator stackable-stable/zookeeper-operator --version 23.7.0 --set kubeletDir=/var/snap/microk8s/common/var/lib/kubelet -n stackable
helm install --wait hdfs-operator stackable-stable/hdfs-operator --version 23.7.0 --set kubeletDir=/var/snap/microk8s/common/var/lib/kubelet -n stackable
helm install --wait commons-operator stackable-stable/commons-operator --version 23.7.0 --set kubeletDir=/var/snap/microk8s/common/var/lib/kubelet -n stackable
helm install --wait secret-operator stackable-stable/secret-operator --version 23.7.0 --set kubeletDir=/var/snap/microk8s/common/var/lib/kubelet -n stackable
```
After the operator's are up and running, the zk.yaml and znode.yaml files(in /HDFS folder at GitHub) are deployed to the Kubernetes cluster.
The namespace `storage` is created for the corresponding files. 
```
kubectl apply -f zk.yaml -n storage
kubectl apply -f znode.yaml -n storage
```
The state of the Zookeeper cluster can be tracked:
```none
kubectl rollout status --watch --timeout=5m statefulset/simple-zk-server-default
```
When the Zookeeper cluster is finished, the HDFS can be deployed with the following command.
`kubectl apply -f hdfs.yaml -n storage`

## Create and enter the hdfs cli

hdfs cli is created with the following cmd with kubectl.
`kubectl run hdfs-cli --rm -i --tty --image apache/hadoop:3 -- bash`

If you want to enter the hdfs cli again in a different terminal, use the following cmd. 
`kubectl exec pods/hdfs-cli --stdin --tty -- bash`

## Look at topics created in HDFS

After creating the Hdfs and Kafka Connect Sink(done in the lower sections), one can then look into the topics file for the SWIRTS_COLLISION partitions made in HDFS with the following cmd inside of the hdfs cli. 
`hdfs dfs -fs hdfs://simple-hdfs-namenode-default-0.storage:8020 -ls`

# Kafka

First creating `kafka` namespace with kubectl, then installing the Strimzi operator within the namespace.
````
helm install -n kafka strimzi-cluster-operator oci://quay.io/strimzi-helm/strimzi-kafka-operator --set watchAnyNamespace=true --set kubeletDir=/var/snap/microk8s/common/var/lib/kubelet -n stackable
````
Wait for the completion of the deployment: `kubectl get pod -n kafka --watch`.

Now to create the Kafka cluster use the Kafka manifest, located within the /Kafka folder at the GitHub project folder
`kubectl apply -n kafka -f kafka.yaml`
Wait for the completion of the Kafka deployment: `kubectl wait kafka/strimzi --for=condition=Ready --timeout=300s -n kafka`.
Then for the extra services needed to interact with Kafka is in the kafka-extra.yaml file. 
`kubectl apply -n kafka -f kafka-extra.yaml`
**Note: KSQL has been removed for being too resource heavy**

The list below summarises the extra services and briefly demonstrate how to interact with them:
- Redpanda 
	- `kubectl port-forward svc/redpanda 8080:8080 -n kafka`. Open [http://127.0.0.1:8080](http://127.0.0.1:8080) in your browser!
- Registry (kafka-schema-registry)
	- `kubectl port-forward svc/kafka-schema-registry 8081:8081 -n kafka`. Make a curl in a terminal [http://127.0.0.1:8081](http://127.0.0.1:8081) and get this output:
- Connect (kafka-connect)
	- `kubectl port-forward svc/kafka-connect 8083:8083 -n kafka`. Make a curl in a terminal [http://127.0.0.1:8083](http://127.0.0.1:8083) and get this output:

## Topics

Currently, there is only the SWIRTS_COLLISION topic created within the Kafka Cluster.

## Kafka Producer

If you want  to produce messages to the Kafka Cluster, then attach your vscode to the Ubuntu pod located in one of the server nodes. Thereafter run the following command to produce messages from the sqlite file into the topics.
`python3 Kafka_producer.py`

## HDFS and Kafka Connect Sink

Configuring a Kafka Connect module to write records from the SWIRTS_COLLISION topic into HDFS.
This is done by using a [HDFS 2 Sink Connector](https://docs.confluent.io/kafka-connectors/hdfs/current/overview.html) developed by Confluent, posting the configuration by using curl in the terminal after Kafka Connect service is port-forwarded to 8083.
`kubectl port-forward svc/kafka-connect 8083:8083 -n kafka`
The configuration for the curl post is located within the HDFS_Setup folder inside of Github, copy paste the cmd within your terminal in accordance with your operating system. 

The post will be made in the HDFS and you can now see the topics created through the hdfs cli. 

# Logs

Written by Kasim, Date: 21/11/2023

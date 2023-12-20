# Install guide for Kafka

First creating `kafka` namespace with kubectl, then installing the Strimzi operator within the namespace

````
helm install -n kafka strimzi-cluster-operator oci://quay.io/strimzi-helm/strimzi-kafka-operator --set watchAnyNamespace=true --set kubeletDir=/var/snap/microk8s/common/var/lib/kubelet -n stackable
````

Wait for the completion of the deployment: `kubectl get pod -n kafka --watch`

Now to create the Kafka cluster use the Kafka manifest, located within the /Kafka folder at the GitHub project folder

`kubectl apply -n kafka -f kafka.yaml`

Wait for the completion of the Kafka deployment: `kubectl wait kafka/strimzi --for=condition=Ready --timeout=300s -n kafka`

Then for the extra services needed to interact with Kafka is in the kafka-extra.yaml file

`kubectl apply -n kafka -f kafka-extra.yaml`

**Note: KSQL has been removed for being too resource heavy**

The list below summarises the extra services and briefly demonstrate how to interact with them:
- Redpanda
	- `kubectl port-forward svc/redpanda 8080:8080 -n kafka`. Open [http://127.0.0.1:8080](http://127.0.0.1:8080) in your browser!
- Registry (kafka-schema-registry)
	- `kubectl port-forward svc/kafka-schema-registry 8081:8081 -n kafka`. Make a curl in a terminal [http://127.0.0.1:8081](http://127.0.0.1:8081) and get this output:
- Connect (kafka-connect)
	- `kubectl port-forward svc/kafka-connect 8083:8083 -n kafka`. Make a curl in a terminal [http://127.0.0.1:8083](http://127.0.0.1:8083) and get this output:

## Kafka Producer

If you want  to produce messages to the Kafka Cluster, then attach your vscode to the Ubuntu pod located in one of the server nodes. Thereafter run the following command to produce messages from the sqlite file into the topics

`python3 Kafka_producer.py`

## HDFS and Kafka Connect Sink

Configuring a Kafka Connect module to write records from the SWIRTS_COLLISION topic into HDFS. This is done by using a [HDFS 2 Sink Connector](https://docs.confluent.io/kafka-connectors/hdfs/current/overview.html) developed by Confluent, posting the configuration by using curl in the terminal after Kafka Connect service is port-forwarded to 8083

`kubectl port-forward svc/kafka-connect 8083:8083 -n kafka`

The configuration for the curl post is located within the HDFS_Setup folder inside of Github, copy paste the cmd within your terminal in accordance with your operating system. 

The post will be made in the HDFS and you can now see the topics created through the HDFS CLI

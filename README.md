# SE07-SP

Software Engineering, 7th semester - Semester Project: Scalable Systems.

# Backlog

Create some data vizs yo

# Useful ShortCuts

Remember, before you can acess the VMs, you need to acess SDU VPN and then follow the guide at its "Before you start" section: https://github.com/jakobhviid/BigDataCourseExercises/blob/main/lectures/04/exercises.md

Also you have to run as root in order to get and see the credentials on your machine.

## HDFS

`kubectl exec pods/hdfs-cli --stdin --tty -- bash`
`export HADOOP_USER_NAME=stackable`.
`hdfs dfs -fs hdfs://simple-hdfs-namenode-default-0.storage:8020 -ls`

## Kafka 
`kubectl port-forward svc/kafka-schema-registry 8080:8080 -n kafka`
`kubectl port-forward svc/kafka-schema-registry 8081:8081 -n kafka`
`kubectl port-forward svc/kafka-connect 8083:8083 -n kafka`

## MongoDB
`kubectl port-forward svc/mongo-express  8084:8084 -n mongodb`

## MinIO 
`kubectl port-forward svc/minio 9001:9001`

## Spark
`kubectl port-forward svc/spark-history-node 18080:18080`

# INSTALL

## Install Guide for HDFS

1. Install with the HDFS Stackable Operators with Healm.

```
helm install --wait zookeeper-operator stackable-stable/zookeeper-operator -n storage --version 23.11.0
helm install --wait hdfs-operator stackable-stable/hdfs-operator -n storage --version 23.11.0
helm install --wait commons-operator stackable-stable/commons-operator -n storage --version 23.11.0
helm install --wait secret-operator stackable-stable/secret-operator -n storage --set kubeletDir=/var/snap/microk8s/common/var/lib/kubelet --version 23.11.0 
helm install --wait listener-operator stackable-stable/listener-operator -n storage --version 23.11.0
```
Note: When using MicroK8s you need to install the secrets-operator using the following option: --set kubeletDir=/var/snap/microk8s/common/var/lib/kubelet.

2. Apply the three yaml files for Zookeeper cluster and HDFS cluster.

`kubectl apply -f zk.yaml -n storage`
`kubectl apply -f znode.yaml -n storage`

After they are complet, the HDFS cluster remains.

`kubectl apply -f hdfs.yaml -n storage`

2. Interact with the HDFS cluster using CLI.

In order to acess and interact withe the files you will need to spin up a interactive container with Ubuntu which should run on the apache/hadoop:3 image.

`kubectl run hdfs-cli --rm -i --tty --image apache/hadoop:3 -- bash`

Afterwards to look up the HDFS files one can use the following command which tells the HDFS CLI to use the HDFS cluster.

`hdfs dfs -fs hdfs://host.namespace:port?`

The host name for the HDFS cluster set up was simple-hdfs-namenode-default-0 and its namespace is storage. This will in turn give the following cmd to utilize.

`hdfs://simple-hdfs-namenode-default-0.storage:8020 -ls`

You also need to use the "stackable" user when interacting with the HDFS cluster. This can be done by setting an environment variable for the current shell session:
`export HADOOP_USER_NAME=stackable`.

### Create and enter the hdfs cli

hdfs cli is created with the following cmd with kubectl.
`kubectl run hdfs-cli --rm -i --tty --image apache/hadoop:3 -- bash`

If you want to enter the hdfs cli again in a different terminal, use the following cmd. 
`kubectl exec pods/hdfs-cli --stdin --tty -- bash`

### Look at topics created in HDFS

After creating the Hdfs and Kafka Connect Sink(done in the lower sections), one can then look into the topics file for the SWIRTS_COLLISION partitions made in HDFS with the following cmd inside of the hdfs cli. 
`hdfs dfs -fs hdfs://simple-hdfs-namenode-default-0.storage:8020 -ls`

## Create a Ubuntu pod which will produce messages to Kafka Cluster.

Simply run the kubectl run... cmd

`kubectl run producer --rm -i -n producer --tty --image ubuntu -- bash`

Though this is not optimial, as when the pod crashes or runs into error, the schedular will send into the shadow realm deleting everything on it.
A yaml file stating a restart policy is a better alternative. 

## Install guide for Kafka

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


### Kafka Producer

If you want  to produce messages to the Kafka Cluster, then attach your vscode to the Ubuntu pod located in one of the server nodes. Thereafter run the following command to produce messages from the sqlite file into the topics.
`python3 Kafka_producer.py`

### HDFS and Kafka Connect Sink

Configuring a Kafka Connect module to write records from the SWIRTS_COLLISION topic into HDFS.
This is done by using a [HDFS 2 Sink Connector](https://docs.confluent.io/kafka-connectors/hdfs/current/overview.html) developed by Confluent, posting the configuration by using curl in the terminal after Kafka Connect service is port-forwarded to 8083.
`kubectl port-forward svc/kafka-connect 8083:8083 -n kafka`
The configuration for the curl post is located within the HDFS_Setup folder inside of Github, copy paste the cmd within your terminal in accordance with your operating system. 

The post will be made in the HDFS and you can now see the topics created through the hdfs cli. 

## Install Guide for MongoDB

1. Create a namespace for mongodb.

`kubectl create namespace mongodb `

2. Apply the YAML manifest file for mongodb.

`kubectl apply -f mongodb.yaml`

3. Get all the resources inside the `mongodb` namespace.

`kubectl port-forward svc/mongo-express  8084:8084 -n mongodb`

## Guide for installing Spark

1. We will be using stackable operators and therefore need to set up a S3 storage for the Spark pods to utilize in storing checkpoints and logs.

Setting up MinIO object store with the following helm chart:

`helm install minio oci://registry-1.docker.io/bitnamicharts/minio --set service.type=NodePort --set defaultBuckets=spark-logs --set auth.rootUser=admin --set auth.rootPassword=password`

To portforward into the MinIO console the following cmd will be used.

`kubectl port-forward svc/minio 9001:9001`

**NOTE**: The MinIO must show ongoing animation at the login screen, at times when you experince none, it is adivsed to shut down the terminal and try portforwarding again which should fix the problem. I have no idea why - Kasim.

Furthermore, a bucket called "spark-logs" will be created and inside it will be a folder called "eventlogs", these are nessary as they are specified in the yaml files for spark to utilize in writing logs to.

2. Apply the spark configuration YAML file.

`kubectl apply -f spark-configurations -n spark`

3. Apply the applicaiton and adjust the drivers resource use.

`kubectl apply -f spark-applicaiton -n spark`

4. Apply the spark history server to get a overlook of DAGs being created and progresison of the applicaiton.

`kubectl apply -f spark-history-server -n spark`

You can portforward and access it by using cmd.

`kubectl port-forward svc/spark-history-node 18080:18080`

## Ubuntu pod for the Full Stack application part of the system

Due to some reason, running the kubctl run... cmd will result in the pod being deleted by the schedular when it enters a error or crashes.
Therefore, a ubuntu.yaml had been created and its restart policy being always.

`kubeclt apply -f ubuntu -n fullstack`

# Logs

Written by Kasim, Date: 18/12/2023
Written by Kasim, Date: 21/11/2023
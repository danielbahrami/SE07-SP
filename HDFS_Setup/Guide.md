# Install Guide for HDFS

Install with the HDFS Stackable Operators with Healm

```
helm install --wait zookeeper-operator stackable-stable/zookeeper-operator -n storage --version 23.11.0
helm install --wait hdfs-operator stackable-stable/hdfs-operator -n storage --version 23.11.0
helm install --wait commons-operator stackable-stable/commons-operator -n storage --version 23.11.0
helm install --wait secret-operator stackable-stable/secret-operator -n storage --set kubeletDir=/var/snap/microk8s/common/var/lib/kubelet --version 23.11.0 
helm install --wait listener-operator stackable-stable/listener-operator -n storage --version 23.11.0
```

Note: When using MicroK8s you need to install the secrets-operator using the following option: --set kubeletDir=/var/snap/microk8s/common/var/lib/kubelet.

Apply the three yaml files for Zookeeper cluster and HDFS cluster

`kubectl apply -f zk.yaml -n storage`
`kubectl apply -f znode.yaml -n storage`

After they are complet, the HDFS cluster remains.

`kubectl apply -f hdfs.yaml -n storage`

Interact with the HDFS cluster using CLI

In order to acess and interact withe the files you will need to spin up a interactive container with Ubuntu which should run on the apache/hadoop:3 image

`kubectl run hdfs-cli --rm -i --tty --image apache/hadoop:3 -- bash`

Afterwards to look up the HDFS files one can use the following command which tells the HDFS CLI to use the HDFS cluster

`hdfs dfs -fs hdfs://host.namespace:port?`

The host name for the HDFS cluster set up was simple-hdfs-namenode-default-0 and its namespace is storage. This will in turn give the following cmd to utilize

`hdfs://simple-hdfs-namenode-default-0.storage:8020 -ls`

You also need to use the "stackable" user when interacting with the HDFS cluster. This can be done by setting an environment variable for the current shell session

`export HADOOP_USER_NAME=stackable`.

# Guide for installing Spark

We will be using stackable operators and therefore need to set up a S3 storage for the Spark pods to utilize in storing checkpoints and logs

Setting up MinIO object store with the following helm chart:

`helm install minio oci://registry-1.docker.io/bitnamicharts/minio --set service.type=NodePort --set defaultBuckets=spark-logs --set auth.rootUser=admin --set auth.rootPassword=password`

To portforward into the MinIO console the following cmd will be used

`kubectl port-forward svc/minio 9001:9001`

**NOTE**: The MinIO must show ongoing animation at the login screen, at times when you experience none, it is advised to shut down the terminal and try portforwarding again which should fix the problem

Furthermore, a bucket called "spark-logs" will be created and inside it will be a folder called "eventlogs", these are necessary as they are specified in the yaml files for spark to utilize in writing logs to

Apply the spark configuration YAML file

`kubectl apply -f spark-configurations -n spark`

Apply the application and adjust the drivers resource use

`kubectl apply -f spark-application -n spark`

Apply the spark history server to get a overlook of DAGs being created and progression of the application

`kubectl apply -f spark-history-server -n spark`

You can portforward and access it by using cmd

`kubectl port-forward svc/spark-history-node 18080:18080`

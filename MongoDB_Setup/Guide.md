# Install Guide for MongoDB

1. Create a namespace for mongodb

`kubectl create namespace mongodb `

2. Apply the YAML manifest file for mongodb

`kubectl apply -f mongodb.yaml`

3. Get all the resources inside the `mongodb` namespace

`kubectl port-forward svc/mongo-express  8084:8084 -n mongodb`

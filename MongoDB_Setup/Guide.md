# Install Guide for MongoDB

Create a namespace for MongoDB

`kubectl create namespace mongodb`

Apply the YAML manifest file for MongoDB

`kubectl apply -f mongodb.yaml`

Get all the resources inside the `mongodb` namespace

`kubectl port-forward svc/mongo-express  8084:8084 -n mongodb`

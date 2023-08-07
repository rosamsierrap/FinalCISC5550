#!/bin/bash
gcloud config set project my-project-cisc5550
gcloud config set compute/zone us-central1-a
gcloud compute instances delete cisc5550-api
gcloud compute firewall-rules delete rule-allow-tcp-5001


gcloud compute instances create cisc5550-api --machine-type n1-standard-1 --image-family debian-10 --image-project debian-cloud --tags http-server --metadata-from-file startup-script=./startup.sh
gcloud compute firewall-rules create rule-allow-tcp-5001 --source-ranges 0.0.0.0/0 --target-tags http-server --allow tcp:5001

export TODO_API_IP=`gcloud compute instances list --filter="name=cisc5550-api" --format="value(EXTERNAL_IP)"`

# next, deploy the app that depens on api
docker build -t rosasierra/cisc5550todoapp --build-arg api_ip=${TODO_API_IP} . #cisc5550todoapp

# docker login
docker push rosasierra/cisc5550todoapp

gcloud container clusters create cisc5550-cluster
kubectl create deployment cc5550 --image=rosasierra/cisc5550todoapp --port=5000
kubectl expose deployment cc5550 --type="LoadBalancer"

kubectl get service cc5550

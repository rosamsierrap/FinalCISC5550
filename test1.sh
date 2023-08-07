#!/bin/bash
gcloud config set project my-project-cisc5550
gcloud config set compute/zone us-east1-b
gcloud compute instances delete cisc5550-api
gcloud compute firewall-rules delete rule-allow-tcp-5001


gcloud compute instances create cisc5550-api --machine-type n1-standard-1 --image-family debian-10 --image-project debian-cloud --tags http-server --metadata-from-file startup-script=./startup.sh
gcloud compute firewall-rules create rule-allow-tcp-5001 --source-ranges 0.0.0.0/0 --target-tags http-server --allow tcp:5001



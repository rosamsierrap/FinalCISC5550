#!/bin/bash

#select project to work on
gcloud config set project my-project-cisc5550

#create the virtual machine instance
gcloud compute instances create instance-2 \
    --machine-type=e2-medium \
    --image-family=debian-10 \
    --image-project=debian-cloud \
    --tags=http-server \
    --zone=us-central1-a
    
#connect to the VM
gcloud compute ssh instance-2 --zone=us-central1-a

#Test the app on Google Cloud
sudo python todolist.py &

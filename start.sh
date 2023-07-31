#!/bin/bash

sudo apt update
sudo apt install python3-pip
pip3 install flask

#Update the last line of the todolist.py file
sed -i 's|app.run("0.0.0.0")|app.run("0.0.0.0", port=80)|' ~/todolist.py

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
gcloud compute ssh instance-2 --zone=us-central1-a << EOF

#installing libraries on the VM
sudo apt update
sudo apt install python3-pip
pip3 install flask
sudo -H pip3 install flask

#Test the app on Google Cloud
sudo python3 todolist.py &

EOF

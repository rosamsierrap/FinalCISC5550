#!/bin/bash

#sudo apt update
#sudo apt install python3-pip
#pip3 install flask

#select project to work on
gcloud config set project my-project-cisc5550

#create the virtual machine instance
gcloud compute instances create instance-2 \
    --machine-type=e2-medium \
    --image-family=ubuntu-2004-lts \
    --image-project=ubuntu-os-cloud \
    --tags=http-server \
    --zone=us-central1-a
    
#connect to the VM
gcloud compute ssh instance-2 --zone=us-central1-a \
   --command="sudo apt update && sudo apt install -y python3-pip && sudo pip3 install flask && sudo -H pip3 install flask
   && git clone https://github.com/rosamsierrap/cisc5550.git && sed -i 's|app.run("0.0.0.0")|app.run("0.0.0.0", port=80)|' todolist.py 
   && sudo python3 ~/todolist.py &"


#installing libraries on the VM
#sudo apt update
#sudo apt install python3-pip
#pip3 install flask
#sudo -H pip3 install flask

#cloning the repository in the virtual machine
#git clone https://github.com/rosamsierrap/cisc5550.git

#Update the last line of the todolist.py file
#sed -i 's|app.run("0.0.0.0")|app.run("0.0.0.0", port=80)|' todolist.py

#Test the app on Google Cloud
#sudo python3 todolist.py &

#EOF

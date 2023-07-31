
:: Set the project to work on
gcloud config set project my-project-cisc5550

:: Create the virtual machine instance
gcloud compute instances create instance-2 ^
    --machine-type=e2-medium ^
    --image-family=ubuntu-2004-lts ^
    --image-project=ubuntu-os-cloud ^
    --tags=http-server ^
    --zone=us-central1-a

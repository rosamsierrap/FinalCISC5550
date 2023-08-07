export TODO_API_IP=`gcloud compute instances list --filter="name=cisc5550-api" --format="value(EXTERNAL_IP)"`

# next, deploy the app that depens on api
docker build -t rosasierra/cisc5550todoapp --build-arg api_ip=${TODO_API_IP} . #cisc5550todoapp

# docker login
docker push rosasierra/cisc5550todoapp

gcloud container clusters create cisc5550-cluster
kubectl create deployment cc5550 --image=rosasierra/cisc5550todoapp --port=5000
kubectl expose deployment cc5550 --type="LoadBalancer"

kubectl get service cc5550

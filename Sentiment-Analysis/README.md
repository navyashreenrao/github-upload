# Steps:
1 Clone the repository from github. Command: git clone https://github.com/rinormaloku/k8s-mastery.git

2 Install npm and mvn on your local system

3 Run ```mvn install``` in sa-webapp to create the jar file 

4 To create docker images of each of these repositories, follow the steps below

5 Open command prompt and navigate to sa-frontend. Use ```npm start```,```npm run build``` to run build the static files. Then use the command ```docker build -f Dockerfile -t navyashree1997/sentiment-analysis-frontend:latest .``` to build the docker image

6 Use ```docker push navyashree1997/sentiment-analysis-frontend:latest``` to push the image to Dockerhub.

7 Open command prompt and navigate to sa-logic. Then use the command ```docker build -f Dockerfile -t navyashree1997/sentiment-analysis-logic:latest .``` to build the docker image

8 Use ```docker push navyashree1997/sentiment-analysis-logic:latest``` to push the image to Dockerhub.

9 Open command prompt and navigate to sa-webapp. Use ```mvn install``` to create the JAR. Then use the command ```docker build -f Dockerfile -t navyashree1997/sentiment-analysis-webapp:latest .``` to build the docker image

10 Use ```docker push navyashree1997/sentiment-analysis-webapp:latest``` to push the image to Dockerhub.

11 We should now push these images to Google Container Registry. To do so, we follow the steps as below on Cloud Shell.

12 We pull the image from dockerhub, give it a tag according to gcp policies and we push the image to the container registry. The commands used are as below
```
docker pull navyashree1997/sentiment-analysis-frontend
docker tag navyashree1997/sentiment-analysis-frontend gcr.io/zippy-world-326315/navyashree1997/sentiment-analysis-frontend:latest
docker push gcr.io/zippy-world-326315/navyashree1997/sentiment-analysis-frontend:latest
docker pull navyashree1997/sentiment-analysis-logic
docker tag navyashree1997/sentiment-analysis-logic gcr.io/zippy-world-326315/navyashree1997/sentiment-analysis-logic:latest
docker push gcr.io/zippy-world-326315/navyashree1997/sentiment-analysis-logic:latest
docker pull navyashree1997/sentiment-analysis-web-app
docker tag navyashree1997/sentiment-analysis-web-app gcr.io/zippy-world-326315/navyashree1997/sentiment-analysis-web-app:latest
docker push gcr.io/zippy-world-326315/navyashree1997/sentiment-analysis-web-app:latest
```

13 We can now see these in the Google Container Registry

14 We should now create a kubernetes cluster to orchestrate these containers. This is done by using the following commands on Cloud shell.
```
gcloud config set project zippy-world-326315
gcloud services enable container.googleapis.com
gcloud container clusters create --machine-type n1-standard-2 --num-nodes 2 --zone us-central1-a --cluster-version latest navyashreekubernetescluster
```

15 Verify that this is done by using ```kubectl get nodes```

16 We start by deloying the sa-logic pod first and then create a load balancing service for the same. The pod is created by going to the container image on the registry and clicking on Deploy. The deployment happens on the cluster we created above by default if no other kubernetes cluster exists. 

17 The sa-logic service is created by clicking on "Expose" under the deployed pod. The target port is given as 5000 and the entry port is 5050. The services can be seen under the "Services and ingress" tab. 

18 We can now deploy sa-web-app by using the end point we got from sa-logic as the environment variable. The env is usually mentioned in the Dockerfile but it can be written while deploying the pod as well. We click on "Deploy" and mention environment variable key as SA_LOGIC_API_URL and value as the end point of sa-logic-service

19 The sa-web-app service is created by clicking on "Expose" under the deployed pod. The port is 8080 for both target and internal port. 

20 We now take the end point of the sa-web-app service and replace the IP address and port number on line 23 in App.js under sa-frontend/src. Run npm run build, update your docker hub image by using docker build -f Dockerfile -t navyashree1997/sentiment-analysis-frontend:latest . and push it to DockerHub using docker push navyashree1997/sentiment-analysis-frontend:latest 

21 Use this image in the GC Container Registry by following the steps mentioned before - pull, tag, push

22 Use this latest image to create the sa-frontend deployment by clicking on the "Deploy" button on the screen. Once this is done, create a service for this deployment using the "Expose" button on the screen. The port numbers are 80 for both the target and the internal values. The sa-frontend-service is now created. 

23 The application can be tested by going to the sa-frontend-service endpoint and typing your text into the text box provided. Press the "Send" button and you can see the l=polarity of the input text. 

24 Disable billing for your GC project after this is done :) 

# Dockerhub URLs:
https://hub.docker.com/repository/docker/navyashree1997/sentiment-analysis-frontend
https://hub.docker.com/repository/docker/navyashree1997/sentiment-analysis-logic
https://hub.docker.com/repository/docker/navyashree1997/sentiment-analysis-web-app

# Steps:
1 The docker images used are present in the following links. Pull each of these images, and push it to you docker hub account by using the following commands. 
By making a copy of the image, we can edit the configurations as we wish, if required. 

Jupyter: https://hub.docker.com/r/navyashree1997/bigdata-jupyter (Pulled from: https://hub.docker.com/r/jupyter/minimal-notebook)

Sonarqube: https://hub.docker.com/r/navyashree1997/sonarscanner (Own image)

Hadoop master: https://hub.docker.com/r/navyashree1997/bigdata-hadoop-namenode (Pulled from: https://hub.docker.com/r/bde2020/hadoop-namenode)

Hadoop datanode: https://hub.docker.com/r/navyashree1997/bigdata-hadoop-datanode (Pulled from : https://hub.docker.com/r/bde2020/hadoop-datanode)

Spark: https://hub.docker.com/r/navyashree1997/bigdata-spark (Pulled from: https://hub.docker.com/r/bitnami/spark)

GUI: https://hub.docker.com/r/navyashree1997/bigdata-terminal-html (Own image)

2 The SonarQube docker image is built by using the Dockerfile present in the sonar folder of this repository. We build, run and push the docker image to our Docker repo.

3 The Terminal docker image is built by using the Dockerfile present in the GUI folder of this repository. We build, run and push the docker image to our Docker repo. This Dockerfile is not complete yet and does not call any Dockerimage upon clicking. This will be done as part of the next checkpoint.

4 We should now push these images to Google Container Registry. To do so, we follow the steps as below on Cloud Shell.

5 We pull the image from dockerhub, give it a tag according to gcp policies and we push the image to the container registry. The commands used are as below
```
docker pull navyashree1997/bigdata-terminal-html
docker tag navyashree1997/bigdata-terminal-html gcr.io/zippy-world-326315/navyashree1997/bigdata-terminal-html:latest
docker push gcr.io/zippy-world-326315/navyashree1997/bigdata-terminal-html:latest

docker pull navyashree1997/bigdata-jupyter
docker tag navyashree1997/bigdata-jupyter gcr.io/zippy-world-326315/navyashree1997/bigdata-jupyter:latest
docker push gcr.io/zippy-world-326315/navyashree1997/bigdata-jupyter:latest

docker pull navyashree1997/sonarscanner
docker tag navyashree1997/sonarscanner gcr.io/zippy-world-326315/navyashree1997/sonarscanner:latest
docker push gcr.io/zippy-world-326315/navyashree1997/sonarscanner:latest

docker pull navyashree1997/bigdata-hadoop-datanode
docker tag navyashree1997/bigdata-hadoop-datanode gcr.io/zippy-world-326315/navyashree1997/bigdata-hadoop-datanode:latest
docker push gcr.io/zippy-world-326315/navyashree1997/bigdata-hadoop-datanode:latest

docker pull navyashree1997/bigdata-hadoop-namenode
docker tag navyashree1997/bigdata-hadoop-namenode gcr.io/zippy-world-326315/navyashree1997/bigdata-hadoop-namenode:latest
docker push gcr.io/zippy-world-326315/navyashree1997/bigdata-hadoop-namenode:latest

docker pull navyashree1997/bigdata-spark
docker tag navyashree1997/bigdata-spark gcr.io/zippy-world-326315/navyashree1997/bigdata-spark:latest
docker push gcr.io/zippy-world-326315/navyashree1997/bigdata-spark:latest
```

6 We can now see these in the Google Container Registry

##Creating Kubernetes Cluster
7 We should now create a kubernetes cluster to orchestrate these containers. This is done by using the following commands on Cloud shell.
```
gcloud config set project zippy-world-326315
gcloud services enable container.googleapis.com
gcloud container clusters create --machine-type n1-standard-2 --num-nodes 2 --zone us-central1-a --cluster-version latest project1kubercluster
```

8 Verify that this is done by using ```kubectl get nodes```

##Deploying the terminal app
9 We start by deloying the terminal pod first and then create a load balancing service for the same. The pod is created by going to the container image on the registry and clicking on Deploy. The deployment happens on the cluster we created above by default if no other kubernetes cluster exists. 

10 The GUI service is created by clicking on "Expose" under the deployed pod. The target port is given as 80 and the entry port is 80. The services can be seen under the "Services and ingress" tab. 

##Deploying Jupyter notebook
11 We next deploy the Jupyter pod and then create a load balancing service for the same. The pod is created by going to the container image on the registry and clicking on Deploy. The deployment happens on the cluster we created above by default if no other kubernetes cluster exists. 

12 The Jupyter service is created by clicking on "Expose" under the deployed pod. The target port is given as 8888 and the entry port is 8888. The services can be seen under the "Services and ingress" tab. 

##Deploying Spark pod
13 We next deploy the Spark pod and then create a load balancing service for the same. The pod is created by going to the container image on the registry and clicking on Deploy. Add an environment variable and give the name as SPARK_MODE and value as master during deployment. The deployment happens on the cluster we created above by default if no other kubernetes cluster exists. 

14 The Spark service is created by clicking on "Expose" under the deployed pod. The target port is given as 8080 and the entry port is 8080. The services can be seen under the "Services and ingress" tab. 

##Deploying the SonarQube pod
15 We next deploy the SonarQube pod and then create a load balancing service for the same. The pod is created by going to the container image on the registry and clicking on Deploy. The deployment happens on the cluster we created above by default if no other kubernetes cluster exists. 

16 The SonarQube service is created by clicking on "Expose" under the deployed pod. The target port is given as 9000 and the entry port is 9000. The services can be seen under the "Services and ingress" tab. 

##Deploying Hadoop data and master nodes
17 We next deploy the Hadoop master pod and then create a load balancing service for the same. The pod is created by going to the container image on the registry and clicking on Deploy. The deployment happens on the cluster we created above by default if no other kubernetes cluster exists. Make sure the deployment is called "namenode". Deploy only one pod for the master. The following environment variable should be set during deployment. 

```
CLUSTER_NAME=mastercluster
CORE_CONF_fs_defaultFS=hdfs://namenode:9000
CORE_CONF_hadoop_http_staticuser_user=root
CORE_CONF_hadoop_proxyuser_hue_groups=*
CORE_CONF_hadoop_proxyuser_hue_hosts=*
CORE_CONF_io_compression_codecs=org.apache.hadoop.io.compress.SnappyCodec
HDFS_CONF_dfs_namenode_datanode_registration_ip___hostname___check=false
HDFS_CONF_dfs_permissions_enabled=false
HDFS_CONF_dfs_webhdfs_enabled=true
```

18 The Hadoop master is created by clicking on "Expose" under the deployed pod. The target port is given as 9870 and the entry port is 9870. Another mapping is added for port 9000. Make sure the service is also called "namenode". The services can be seen under the "Services and ingress" tab. 

19 We next deploy the Hadoop datanode pod. The pod is created by going to the container image on the registry and clicking on Deploy. The deployment happens on the cluster we created above by default if no other kubernetes cluster exists. Make sure the deployment is called "datanode". Deploy 2 pods for the datanodes. The following environment variable should be set during deployment.

```
SERVICE_PRECONDITION=http://namenode:9870
CORE_CONF_fs_defaultFS=hdfs://namenode:9000
CORE_CONF_hadoop_http_staticuser_user=root
CORE_CONF_hadoop_proxyuser_hue_groups=*
CORE_CONF_hadoop_proxyuser_hue_hosts=*
CORE_CONF_io_compression_codecs=org.apache.hadoop.io.compress.SnappyCodec
HDFS_CONF_dfs_namenode_datanode_registration_ip___hostname___check=false
HDFS_CONF_dfs_permissions_enabled=false
HDFS_CONF_dfs_webhdfs_enabled=true
```
20 We can see each of these services running on their specific end points as demonstrated in the screenshots. We can also see all the pods running in our Kubernetes cluster.

##Redeploying the UI terminal 

21 Once the services are created, we need to add the service endpoints for each of these pods into the UI terminal so the user can be redirected to the right application upon clicking the button. 

22 We do this by adding the href option in the HTML source code of the UI

23 This docker image should now be updated with the new data. Use the following commands again to build and push the Docker image onto Dockerhub. Navigate to the folder where the Dockerfile for the UI is present and execute the follwoing commands.
```
docker build -t navyashree1997/bigdata-terminal-html
docker push navyashree1997/bigdata-terminal-html
```
24 This will update the Dockerhub image but it should be pulled into our GCP Container Registry. This can be done by re-running the first three commands on step 5

21 Disable billing for your GC project after this is done :) 

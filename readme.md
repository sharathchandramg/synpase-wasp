# About

This is the minimum repository for running spark jobs on azure synapse.


## Build

Build Python package.

```bash
poetry build --format wheel
```

Build and push Docker image.

```bash
az acr login --name cueboxdev
docker build -t cueboxdev.azurecr.io/wasp:latest .
docker push cueboxdev.azurecr.io/wasp:latest
```


## Run via Kubernetes API

Pre-requisites:
* `spark` service account with appropriate Kubernetes permissions.

(Master URL will be different when running from Prefect.)

```bash
spark-submit \
--master k8s://https://cuebox-dev-cuebox-dev-rg-6aafc6-59873917.hcp.westus2.azmk8s.io:443 \
--deploy-mode cluster \
--name wasp \
--conf spark.executor.instances=3 \
--conf spark.kubernetes.container.image=cueboxdev.azurecr.io/wasp:latest \
--conf spark.kubernetes.namespace=cuebox \
--conf spark.kubernetes.authenticate.driver.serviceAccountName=spark \
--conf spark.kubernetes.driver.podTemplateFile=k8s/template.yaml \
--conf spark.kubernetes.executor.podTemplateFile=k8s/template.yaml \
--conf spark.hadoop.fs.azure.account.auth.type=OAuth \
--conf spark.hadoop.fs.azure.account.oauth.provider.type=org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider \
--conf "spark.hadoop.fs.azure.account.oauth2.client.endpoint=https://login.microsoftonline.com/<tenant>/oauth2/token" \
--conf spark.hadoop.fs.azure.account.oauth2.client.id=<client> \
--conf "spark.hadoop.fs.azure.account.oauth2.client.secret=<secret>" \
local:///opt/application/jobs/participant.py
```

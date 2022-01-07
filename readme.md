# About

This is the minimum repository for running spark jobs on azure synapse.

## Steps

Create conda environment from environment.yml

```
conda env create --file environment.yml
```

Create a conda pack

```
conda pack -f -o dist/wasp_conda_env.tar.gz --ignore-editable-packages
```

Run Locally

```
spark-submit --master "local[3]" --archives dist/wasp_conda_env.tar.gz  wasp/jobs/participant.py
```

Run on synapse

1. Upload the package `wasp_conda_env.tar.gz` to ABS
2. Upload the spark job `wasp/jobs/pariticipant.py` to ABS
3. Create a spark job defintion under synapse with main file as `pariticipant.py`
4. Run the submit via CLI as

```
az synapse spark job submit --workspace-name <> --spark-pool-name <> --executor-size Small --executors 2 --language PySpark --main-definition-file abfss://<>/participant.py --name <job_name> --archives abfss://<>/wasp_conda_env.tar.gz
```

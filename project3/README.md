PART1 - build the pipeline
PART2 - [create the stack](https://medium.com/@kattsonbastos/mlops-with-zenml-and-mlflow-how-can-we-build-a-model-training-pipeline-a-practical-example-6a5f24f5eefc)
```
zenml experiment-tracker register mlflow_tracker --type=mlflow --flavor=mlflow
zenml stack register mlflow_stack \
    -e mlflow_tracker \
    -a default \
    -o default 
mlflow ui --backend-store-uri file:/home/<user>/.config/zenml/local_stores/123/mlruns
```
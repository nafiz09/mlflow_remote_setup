import mlflow
import os

output_dir = "outputs"
os.makedirs(output_dir, exist_ok=True)
info_path = os.path.join(output_dir, "info.txt")

with open(info_path, "w") as f:
    f.write("This is an example artifact.\nAccuracy: 0.85")


mlflow.log_param("learning_rate", 0.01)
mlflow.log_param("epochs", 10)

# Log a metric
mlflow.log_metric("accuracy", 0.85)

# Log the artifact folder (better than individual files)
mlflow.log_artifacts(output_dir)
mlflow.log_artifact("model_plot.png")
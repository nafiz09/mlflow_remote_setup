import mlflow
import os
import sys

# Set MLflow server URI
mlflow.set_tracking_uri("http://192.168.10.44:3050")
mlflow.set_experiment("logging_example_experiment")

# Optional: Set S3 credentials (only if not already set in env or ~/.aws/credentials)
os.environ["AWS_ACCESS_KEY_ID"] = os.getenv("AWS_ACCESS_KEY_ID", "minio")
os.environ["AWS_SECRET_ACCESS_KEY"] = os.getenv("AWS_SECRET_ACCESS_KEY", "minio123")
os.environ["MLFLOW_S3_ENDPOINT_URL"] = os.getenv("MLFLOW_S3_ENDPOINT_URL", "http://192.168.10.44:9000")

# Create an output directory and write a sample file
output_dir = "outputs"
os.makedirs(output_dir, exist_ok=True)
info_path = os.path.join(output_dir, "info.txt")

with open(info_path, "w") as f:
    f.write("This is an example artifact.\nAccuracy: 0.85")

try:
    with mlflow.start_run() as run:
        # Log parameters
        mlflow.log_param("learning_rate", 0.01)
        mlflow.log_param("epochs", 10)

        # Log a metric
        mlflow.log_metric("accuracy", 0.85)

        # Log the artifact folder (better than individual files)
        mlflow.log_artifacts(output_dir)

        print("✅ Parameters, metric, and artifact logged.")
        print(f"🔗 View run at: {mlflow.get_tracking_uri()}/#/experiments/{run.info.experiment_id}/runs/{run.info.run_id}")

except Exception as e:
    print("❌ Failed to log to MLflow:", e)
    sys.exit(1)

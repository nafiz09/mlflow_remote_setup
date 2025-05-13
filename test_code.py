# Import MLflow
import mlflow

# Create new experiment
mlflow.create_experiment("Unicorn Model")

# Tag new experiment
mlflow.set_experiment_tag("version", "1.0")

# Set the experiment
mlflow.set_experiment("Unicorn Model")

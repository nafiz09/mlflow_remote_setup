# Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir mlflow psycopg2-binary boto3

# Default command
CMD ["mlflow", "server", \
     "--backend-store-uri=postgresql://POSTGRES_USER:POSTGRES_PASSWORD@postgres:5432/mlflow_db", \
     "--default-artifact-root=s3://mlflow/", \
     "--host=0.0.0.0", \
     "--port=3050"]

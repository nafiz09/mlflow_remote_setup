# MLflow Remote Server Setup

This project sets up a **remote MLflow server** using Docker Compose. It includes:

- **PostgreSQL** as the backend store for MLflow metadata.
- **MinIO** as the artifact store for model outputs and other files.
- **MLflow Tracking Server** running in a Docker container.
- A simple Python example to demonstrate logging parameters, metrics, and artifacts to the remote MLflow server.

---

## 📦 Project Structure

```
.
├── docker-compose.yml          # Defines services: PostgreSQL, MinIO, MLflow server
├── Dockerfile                  # Custom Dockerfile for MLflow server
├── simple_logging_example.py  # Example script to log to the MLflow server
└── README.md                   # You are here
```

---

## 🚀 Getting Started

### 1. Prerequisites

- Docker and Docker Compose installed
- Open ports `3050`, `5432`, `9000`, and `9001` (or adjust in `docker-compose.yml`)
- Python 3.x (for the example script)

---

### 2. Configuration Overview

| Component  | Purpose                     | Port | Credentials               |
|------------|-----------------------------|------|---------------------------|
| PostgreSQL | MLflow backend store        | 5432 | `mlflow_user` / `mlflow_pass` |
| MinIO      | MLflow artifact store       | 9000 | `minio` / `minio123`      |
| MLflow     | Tracking UI & API server    | 3050 | N/A                       |

Artifacts are stored in `/mnt/drive1/mlflow` and PostgreSQL data in `/home/ssclml/mlflow_postgres`.

---

### 3. Start the Services

```bash
docker-compose up -d --build
```

Wait for the services to initialize.

---

### 4. Access the Services

- **MLflow UI**: [http://localhost:3050](http://localhost:3050)
- **MinIO Console**: [http://localhost:9001](http://localhost:9001)

---

### 5. Run the Logging Example

> Make sure environment variables match your local setup or edit them in the script.

```bash
python simple_logging_example.py
```

This will:
- Log parameters and a metric
- Upload an example artifact and image
- Print a link to view the run in the MLflow UI

---

## 🐳 Dockerfile Overview

The `Dockerfile` builds a container that launches the MLflow server and connects it to the PostgreSQL and MinIO services using environment variables:

```Dockerfile
CMD mlflow server     --backend-store-uri postgresql://mlflow_user:mlflow_pass@postgres:5432/mlflow_db     --default-artifact-root s3://mlflow/     --host 0.0.0.0     --port 3050
```

---

## 📁 Volumes and Data Persistence

- **PostgreSQL Data**: `/home/ssclml/mlflow_postgres`
- **MinIO Buckets**: `/mnt/drive1/mlflow`
  - These ensure your experiment metadata and artifacts persist across container restarts.

---

## 🛠 Environment Variables Summary

| Variable               | Value                  | Used By     |
|------------------------|------------------------|-------------|
| `POSTGRES_DB`          | `mlflow_db`            | PostgreSQL  |
| `POSTGRES_USER`        | `mlflow_user`          | PostgreSQL  |
| `POSTGRES_PASSWORD`    | `mlflow_pass`          | PostgreSQL  |
| `MINIO_ROOT_USER`      | `minio`                | MinIO       |
| `MINIO_ROOT_PASSWORD`  | `minio123`             | MinIO       |
| `AWS_ACCESS_KEY_ID`    | `minio`                | MLflow & client |
| `AWS_SECRET_ACCESS_KEY`| `minio123`             | MLflow & client |
| `MLFLOW_S3_ENDPOINT_URL` | `http://minio:9000`  | MLflow & client |

---

## 📌 Notes

- MLflow uses **S3-style URIs** for artifact storage (e.g., `s3://mlflow/`).
- Ensure `mlflow` bucket exists in MinIO or configure MLflow to create it automatically.
- The `simple_logging_example.py` script assumes the server is accessible at `192.168.10.44`. Adjust this to your actual host IP or `localhost` if running locally.

---

## 🧼 Teardown

To stop and remove containers:

```bash
docker-compose down
```

To also remove volumes:

```bash
docker-compose down -v
```

---

## 📚 References

- [MLflow Documentation](https://mlflow.org/docs/latest/index.html)
- [MinIO Documentation](https://min.io/docs/)
- [Docker Compose](https://docs.docker.com/compose/)
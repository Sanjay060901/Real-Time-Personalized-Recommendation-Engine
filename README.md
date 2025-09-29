# Real-Time Personalized Recommendation Engine

## 📌 Overview

This project demonstrates an **end-to-end real-time data engineering pipeline** for an **e-commerce recommendation system**. It simulates user events (views, clicks, purchases), ingests them via **Kafka**, processes them with **Spark Structured Streaming**, stores results in a **Delta Lake**, builds user-level features with **Feast**, trains a simple recommendation model, and serves real-time recommendations through a **FastAPI API** with **Redis caching**.

The design mimics a modern **Lakehouse + MLOps** architecture while staying lightweight enough to run locally using **Docker Compose**.

---

## 🏗️ Architecture

**Steps:**

1. **Event Ingestion:** Kafka producer emits user activity events (simulated).
2. **Streaming ETL:** Spark Structured Streaming consumes events and writes to Delta Lake.
3. **Feature Store:** Simple aggregation ingested into Postgres (Feast-compatible offline store).
4. **Model Training:** A naive popularity-based recommender is trained and serialized.
5. **Serving Layer:** FastAPI app exposes `/recommend` endpoint with Redis caching.
6. **Orchestration:** Airflow DAG provided for feature ingestion + model retraining.

**Tech Stack:**

* Kafka (event streaming)
* Spark Structured Streaming + Delta Lake (real-time ETL)
* Feast (feature store)
* Postgres (offline store)
* Redis (online cache)
* FastAPI (model serving)
* MLflow (optional experiment tracking)
* Airflow (orchestration)

---

## 📂 Repo Structure

```
realtime-reco/
├── docker-compose.yml         # Local infra (Kafka, Redis, Postgres)
├── kafka/producer.py          # Event generator for Kafka
├── streaming/spark_stream.py  # Spark job → Delta Lake
├── storage/write_delta.py     # (Optional helper script)
├── features/
│   ├── feature_store.yaml     # Feast config
│   └── ingest_features.py     # Aggregates → Postgres
├── ml/
│   ├── train_model.py         # Simple popularity-based recommender
│   └── model_utils.py         # Utilities (future expansion)
├── serving/app.py             # FastAPI + Redis model serving
├── orchestration/airflow_dag_reco.py  # Example DAG for automation
├── requirements.txt           # Python dependencies
├── README.md                  # Project overview (this file)
└── README_RUN.md              # Detailed run instructions
```

---

## 🚀 Quick Start

### 1. Setup

```bash
git clone <your-repo-url>
cd realtime-reco
pip install -r requirements.txt
docker compose up -d
```

### 2. Create Kafka Topic

```bash
docker exec -it $(docker ps --filter "ancestor=confluentinc/cp-kafka:7.4.0" -q) \
  kafka-topics --create --topic user_events --bootstrap-server kafka:9092 \
  --replication-factor 1 --partitions 3
```

### 3. Run Components

```bash
# 1. Start event producer
python kafka/producer.py

# 2. Start Spark streaming job
python streaming/spark_stream.py

# 3. Ingest features into Postgres
python features/ingest_features.py

# 4. Train model
python ml/train_model.py

# 5. Serve API
python serving/app.py
```

### 4. Test API

```bash
curl -X POST http://localhost:8000/recommend \
  -H 'Content-Type: application/json' \
  -d '{"user_id":"u1"}'
```

---

## 📊 Example Output

```json
{
  "user_id": "u1",
  "recs": ["p2", "p1", "p4"]
}
```

---

## 🔧 Production Enhancements

* Replace local Kafka with **AWS MSK / Confluent Cloud**.
* Store Delta tables on **S3/ADLS/GCS**.
* Register Feast entities + feature views, materialize to Redis online store.
* Train robust models (ALS, neural recommenders) and serve via **TensorFlow Serving** or **SageMaker**.
* Use **Databricks MLflow** for model versioning.
* Add monitoring (Prometheus, Grafana) + alerts.

---

## 📚 References

* [Apache Kafka](https://kafka.apache.org/)
* [Delta Lake](https://delta.io/)
* [Apache Spark](https://spark.apache.org/)
* [Feast Feature Store](https://feast.dev/)
* [FastAPI](https://fastapi.tiangolo.com/)
* [MLflow](https://mlflow.org/)
* [Airflow](https://airflow.apache.org/)

---

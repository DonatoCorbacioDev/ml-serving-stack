# ML Serving Stack

Containerized Machine Learning serving workflow using Docker, FastAPI and Docker Compose.

This project demonstrates a simple production-oriented ML pipeline with:

- training container
- persistent model artifact
- FastAPI inference service
- Docker Compose orchestration

The goal is to understand the fundamentals of ML serving, containerization and MLOps basics.

---

# Architecture

```text
training container
↓
model.joblib
↓
FastAPI serving container
↓
/predict endpoint
```

The system separates:

- model training
- artifact persistence
- inference serving

using independent Docker containers.

---

# Tech Stack

- Python
- scikit-learn
- FastAPI
- Docker
- Docker Compose
- joblib

---

# Project Structure

```text
ml-serving-stack/
│
├── training/
│   ├── train.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── api/
│   ├── main.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── data/
│   └── models/
│
├── docs/
│   ├── docker_week1.md
│   └── docker_week2.md
│
├── docker-compose.yml
└── README.md
```

---

# Quick Start

## 1. Train the model

```bash
docker compose --profile train run --rm training
```

This generates:

```text
data/models/model.joblib
```

---

## 2. Start the API

```bash
docker compose up api
```

API available at:

```text
http://localhost:8000
```

---

# API Endpoints

## Healthcheck

```bash
curl http://localhost:8000/health
```

---

## Prediction

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [5.1, 3.5, 1.4, 0.2]}'
```

---

## Swagger Docs

```text
http://localhost:8000/docs
```

---

# Key Concepts Practiced

- Docker containerization
- Layer caching
- Bind mounts
- Persistent ML artifacts
- FastAPI model serving
- Docker Compose orchestration
- Container networking
- Read-only volumes

---

# Current Limitations

The model is currently loaded at every request inside `/predict`.

This is acceptable for learning purposes,
but not optimal for production systems.

In real-world applications the model is usually loaded once during API startup and kept in memory.

---

# Learning Goals

This repository is part of a hands-on learning path focused on:

- ML Engineering
- Docker
- API serving
- deployment workflows
- MLOps fundamentals
# ML Serving Stack

Containerized Machine Learning serving workflow using Docker, FastAPI, Docker Compose and GitHub Actions.

This project demonstrates a production-oriented ML serving workflow with:

* training container
* persistent ML artifact
* FastAPI inference service
* Docker Compose orchestration
* GitHub Actions CI/CD
* GitHub Container Registry (GHCR)

The goal is to understand the fundamentals of:

* ML serving
* containerization
* deployment workflows
* CI/CD
* MLOps foundations

---

# Architecture

```text
training container
↓
persistent ML artifact
↓
FastAPI serving container
↓
GitHub Actions CI/CD
↓
GitHub Container Registry
↓
docker pull / docker run
```

The system separates:

* model training
* artifact persistence
* inference serving
* image publishing

using independent Docker workflows.

---

# Tech Stack

* Python
* scikit-learn
* FastAPI
* Docker
* Docker Compose
* GitHub Actions
* GitHub Container Registry (GHCR)
* joblib

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
│   ├── docker_week2.md
│   ├── docker_week3.md
│   └── docker_week4.md
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── docker-compose.yml
├── .gitignore
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

# CI/CD Pipeline

The repository includes a GitHub Actions workflow that:

* builds the FastAPI Docker image
* publishes the image to GitHub Container Registry
* enables image portability across environments

Workflow file:

```text
.github/workflows/ci.yml
```

Published image:

```text
ghcr.io/donatocorbaciodev/ml-api:latest
```

---

# Running the Published Image

Pull image from GHCR:

```bash
docker pull ghcr.io/donatocorbaciodev/ml-api:latest
```

Run container with mounted ML artifact:

```bash
docker run --rm -p 8000:8000 \
  -v "$(pwd)/data/models:/data/models:ro" \
  ghcr.io/donatocorbaciodev/ml-api:latest
```

---

# Key Concepts Practiced

* Docker containerization
* Layer caching
* Bind mounts
* Persistent ML artifacts
* FastAPI model serving
* Docker Compose orchestration
* Container networking
* Read-only volumes
* Docker HEALTHCHECK
* Non-root containers
* Docker Scout vulnerability scanning
* GitHub Actions CI/CD
* Container registry publishing
* ML artifact separation

---

# Production-Oriented Features

The project includes several production-oriented practices:

* startup model loading
* container health monitoring
* non-root container execution
* vulnerability scanning
* CI/CD automation
* image publishing workflow
* artifact separation from application image

---

# Current Scope

The repository currently focuses on:

* Docker-based ML serving
* local deployment workflows
* CI/CD fundamentals
* ML artifact management
* container lifecycle understanding

Advanced orchestration technologies such as Kubernetes are intentionally out of scope at this stage.

---

# Learning Goals

This repository is part of a hands-on learning path focused on:

* ML Engineering
* Docker
* API serving
* deployment workflows
* CI/CD
* MLOps fundamentals

---

# Future Improvements

Possible future extensions:

* forecasting model serving
* model versioning
* automated testing
* MLflow integration
* cloud deployment
* Kubernetes orchestration
* GPU-based inference

# Project — AI / YoloGK Serving API (multi-platform ML deployment, 2026)

## Overview
YoloGK serves the GalleryKeeper YOLO11 detection model, trained by Narymane, through a REST API, following the "write once, deploy everywhere" principle: the same model and the same application code are deployed on CPU, on NVIDIA Jetson Nano and on Kubernetes / OpenShift. Only the Dockerfile and the deployment configuration change per target.

## 3-Tier Architecture
- Nginx as the front end
- FastAPI API running the YOLO11 model through ONNX Runtime
- PostgreSQL 16 database

## Target 1 — CPU (yoloGK-serving-api)
GitHub: https://github.com/chabanenary/yoloGK-serving-api
- FastAPI API serving the YOLO11 model through ONNX Runtime (CPU)
- Containerized with Docker; Docker / Podman Compose
- Automatic Swagger documentation at /docs
- Tests with pytest
- Stack: Python, FastAPI, ONNX Runtime, Pillow, Docker, pytest

## Target 2 — NVIDIA Jetson Nano GPU (yoloGK-jetson-serving-api)
GitHub: https://github.com/chabanenary/yoloGK-jetson-serving-api
- Same FastAPI application, adapted to the Jetson Nano
- GPU-accelerated inference through ONNX Runtime with CUDA / TensorRT
- Based on the NVIDIA L4T (Linux for Tegra) Docker image, container with the nvidia runtime
- Automatic GPU detection: CUDA if available, CPU fallback otherwise
- Optimized for constrained hardware (4 GB of RAM, Maxwell GPU), with FPS profiling under thermal constraints

## Target 3 — Kubernetes and OpenShift on AWS (yoloGK-kubernetes-serving-api)
GitHub: https://github.com/chabanenary/yoloGK-kubernetes-serving-api
- Kubernetes and OpenShift deployed on an AWS server
- Manifests organized with kustomize: Deployment with replicas, HPA (horizontal autoscaling), liveness / readiness probes, resource limits
- NetworkPolicy, persistent volumes (PV / PVC), ClusterIP Service
- External access through a Kubernetes ingress and an OpenShift route

## API Endpoints (common to all deployments)
- GET /health — liveness probe, reports the model status
- GET /device — GPU / CUDA availability and active inference provider
- POST /classify — classifies one image (upload + confidence threshold)
- POST /classify/batch — classifies several images in one request, with per-image results and a summary

## What This Proves
Narymane can take an ML model she trained and deploy it across the full spectrum of environments: local development (CPU), GPU edge device (Jetson Nano) and cloud orchestration (Kubernetes / OpenShift on AWS), with a complete 3-tier architecture. This is exactly the skill set expected from an ML deployment or MLOps engineer.

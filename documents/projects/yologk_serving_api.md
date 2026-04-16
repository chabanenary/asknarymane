# Project — AI/ YoloGK Serving API (Multi-Platform ML Deployment)

## Overview
A suite of projects demonstrating multi-platform deployment of Narymane's custom-trained YOLO11 GalleryKeeper model via a REST API. The same model and application code are deployed across three different environments, showcasing MLOps best practices.

## Three Deployment Targets

### 1. yoloGK-serving-api — CPU/Mac Deployment
GitHub: https://github.com/chabanenary/yoloGK-serving-api

- FastAPI REST API serving the GalleryKeeper YOLO11 model
- ONNX Runtime for inference (CPU)
- Containerized with Docker
- Designed for development, testing, and cloud deployment
- Endpoints: /health, /device, /classify, /classify/batch
- Automatic Swagger documentation at /docs
- Tests with pytest

Tech stack: Python, FastAPI, ONNX Runtime, Pillow, Docker, pytest

### 2. yoloGK-jetson-serving-api — Jetson Nano GPU Deployment
GitHub: https://github.com/chabanenary/yoloGK-jetson-serving-api

- Same FastAPI application adapted for NVIDIA Jetson Nano
- GPU-accelerated inference via ONNX Runtime with CUDA/TensorRT
- Based on NVIDIA L4T (Linux for Tegra) Docker image
- Automatic GPU detection: uses CUDA if available, falls back to CPU
- Optimized for constrained hardware (4GB RAM, Maxwell GPU)
- Docker container with nvidia runtime

Tech stack: Python, FastAPI, ONNX Runtime GPU, CUDA, TensorRT, Docker, NVIDIA L4T

### 3. yoloGK-kubernetes-serving-api — Kubernetes/OpenShift Deployment
GitHub: https://github.com/chabanenary/yoloGK-kubernetes-serving-api

- Kubernetes deployment manifests for the serving API
- Deployment with replicas, resource limits, liveness/readiness probes
- Service configuration with ClusterIP
- OpenShift Route for external access
- Designed for production-grade orchestrated deployment

Tech stack: Kubernetes, OpenShift, Docker, YAML manifests

## API Endpoints (common to all deployments)
- GET /health — Liveness probe, reports model status
- GET /device — Returns GPU/CUDA availability and active inference provider
- POST /classify — Classify a single image (upload + confidence threshold)
- POST /classify/batch — Classify multiple images in one request, returns per-image results and summary

## Architecture
The model (ONNX format) is identical across all three deployments. The application code (FastAPI + inference logic) is also identical. Only the Dockerfile and deployment configuration change per target. This demonstrates a key MLOps pattern: write once, deploy everywhere.

## What This Proves
Narymane can take a trained ML model and deploy it across the full spectrum of environments: local development (Mac/CPU), edge device with GPU (Jetson Nano), and cloud orchestration (Kubernetes/OpenShift). This is exactly the skillset expected of an ML deployment engineer or MLOps engineer.

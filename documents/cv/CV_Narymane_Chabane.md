# Narymane Chabane

**AI/ML Engineer | Embedded Linux & Edge AI | MLOps**

Sanary-sur-Mer, France | chabanenarymane@gmail.com | [LinkedIn](https://www.linkedin.com/in/narymane-chabane/) | [GitHub](https://github.com/chabanenary) | [asknarymane.com](https://asknarymane.com)

---

## Profile

AI/ML engineer with 12+ years of embedded systems R&D experience, now building production-grade AI applications. Deep expertise in LLM serving, RAG pipelines, ML model deployment on edge and cloud, and full-stack AI application development. Strong systems-level thinking, production mindset, and hands-on experience across the full ML lifecycle — from model training to Kubernetes deployment.

---

## AI/ML Skills

| Domain | Technologies |
|--------|-------------|
| **LLM & RAG** | Ollama, Groq API, LangChain, ChromaDB, nomic-embed-text, prompt engineering, conversation management |
| **AI Agents** | MCP (Model Context Protocol), tool calling, multi-agent routing, intent detection |
| **ML / Deep Learning** | YOLO11 (training, optimization), TensorFlow/TFLite, ONNX, OpenCV |
| **ML Serving** | FastAPI, ONNX Runtime (CPU & GPU), TensorRT |
| **MLOps & DevOps** | Docker, Kubernetes, OpenShift, GitHub Actions, CI/CD pipelines |
| **Programming** | Python (5+ years, advanced), C (10+ years, expert), Bash, Java |
| **Edge / Embedded** | NVIDIA Jetson Nano, ARM SoCs, Linux kernel, Yocto, VxWorks RTOS |

---

## AI Projects

### AskNarymane — RAG Chatbot for Recruiters
[asknarymane.com](https://asknarymane.com) | [GitHub](https://github.com/chabanenary/asknarymane)

Production-deployed RAG chatbot with intelligent multi-agent system.

- **RAG pipeline**: bilingual document ingestion, ChromaDB vector search, re-ranking, context compression
- **4 agents**: profile RAG, real-time GitHub API, contact facilitation, job matching analysis
- **LLM integration**: dual-provider (Ollama local / Groq cloud), model switching at runtime
- **Stack**: Python, FastAPI, Next.js, ChromaDB, Docker, Railway.app
- **Deployment**: dual-mode architecture (Docker Compose dev / Railway prod), auto-ingestion, CORS management

### YoloGK Serving API — Multi-Platform ML Deployment
[GitHub](https://github.com/chabanenary/yoloGK-serving-api)

ML model serving across 3 environments with identical codebase.

- **CPU/Cloud**: FastAPI + ONNX Runtime, Docker, pytest
- **Edge GPU**: NVIDIA Jetson Nano, CUDA/TensorRT acceleration, NVIDIA L4T
- **Orchestration**: Kubernetes/OpenShift with replicas, probes, resource limits
- Write once, deploy everywhere — key MLOps pattern demonstrated

### GalleryKeeper — On-Device AI for Privacy
[GitHub](https://github.com/chabanenary/GalleryKeeper-App) | [Training Pipeline](https://github.com/chabanenary/Yolo11_training_GK) | [Blog](https://dev.to/chabanenary) | [Demo EN](https://www.youtube.com/watch?v=jnUaWvC-wpw) | [Demo FR](https://www.youtube.com/watch?v=V_BQd_TGrLw)

Privacy-first Android app that detects and organizes sensitive photos (nudity, children, ID documents, credit cards) using a custom-trained YOLO11 model — 100% offline, zero cloud uploads.

- **First Android app**, entirely self-taught (Java, Android SDK, MVVM architecture, Room database)
- **Custom YOLO11 model** trained from scratch: dataset curation & annotation (1,400+ images, 4 classes), training with Ultralytics, evaluation, quantization, TFLite export
- **On-device inference** with TFLite — real-time classification, no internet required
- **Background monitoring** via Android foreground service with notifications
- **Privacy by design**: uses MediaStore API, photos never leave the device, user confirms all actions
- **Full ML pipeline**: data collection → annotation → training → optimization → mobile deployment → serving API (YoloGK)
- Published technical blog post on Dev.to detailing the full learning journey

---

## Professional Experience

### Embedded Linux R&D Engineer — Ekinops / OneAccess, Paris (2011–2020)
- Led development of Virtual CPE solution (vCPE) on x86 platforms — Linux, Docker containers, CI/CD
- Developed and maintained Linux-based firmware for telecom-grade CPE devices (routers, gateways)
- BSP development, kernel configuration, Yocto/OpenEmbedded build systems
- Coordinated offshore development teams, code reviews, technical documentation

### Embedded Software Engineer — Eolices, Paris (2007–2011)
- VxWorks RTOS firmware development for network equipment
- Real-time multitasking, interrupt handling, device drivers (Ethernet, SFP, Wi-Fi, 4G)
- U-Boot bootloader porting and customization

### Intern — STMicroelectronics, Paris (2006–2007)
- Embedded software development during Télécom Paris Master's program

---

## Education

- **Master — Télécom Paris** (2006) — Communication Devices & Techniques, First Class Honours
- **Engineering — École Nationale Polytechnique d'Alger** (2000–2005) — Electronics & Telecommunications, First Class Honours
- **Continuous learning** — Hands-On ML (Aurélien Géron), Generative AI MOOCs, self-taught in FastAPI, Docker, Kubernetes

---

## Languages

- French (native) | Arabic (native) | English (fluent)

---

## Publications

- [Building GalleryKeeper: an AI-powered Android app](https://dev.to/chabanenary) — Dev.to technical blog post
- Open source contributor — all AI/ML projects published on GitHub

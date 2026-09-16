# Embedded Multimodal AI — Freelance Mission

## Context
Since June 2026, Narymane has been working as a freelancer on an embedded multimodal AI product built on NVIDIA Jetson Orin Nano Super 8GB. She is involved from POC to prototype, with end-to-end product responsibility: hardware selection, software architecture, and AI model choices.

## Role & Responsibilities
- End-to-end design and development of an embedded multimodal AI system
- Contributing to hardware choices (edge platform, sensors, audio, video)
- Defining the system's software architecture (edge + cloud)
- Selecting, evaluating, and integrating AI models (STT, vision, LLM, TTS)
- Building the complete real-time pipeline: capture → analysis → inference → output
- Performance optimization under resource constraints (8 GB RAM, shared GPU, thermal management)

## Architecture & Technical Skills

### Edge Computing (Jetson Orin Nano)
- Asynchronous multi-threaded orchestration (Python asyncio + threads)
- Real-time audio pipeline: microphone capture, echo cancellation (PipeWire AEC), voice activity detection (Silero VAD)
- On-device Speech-to-Text with Whisper running on GPU
- Voice prosody analysis (Librosa) for user state assessment
- Computer vision: webcam capture (OpenCV), multimodal vision model inference (Qwen-VL via llama.cpp on GPU)
- Advanced audio management: PipeWire, hardware echo cancellation, audio streaming, barge-in mechanism (real-time user interruption)
- Thermal monitoring and GPU/RAM resource management

### Hybrid Edge-Cloud Architecture
- Real-time bidirectional communication via Socket.IO
- Relay gateway between edge components and cloud services
- Cloud LLM integration (Gemini) with context caching for cost optimization
- Cloud text-to-speech with audio streaming back to edge
- React frontend with 3D rendering (Three.js) and lip-sync

### DevOps & Embedded Deployment
- Automated Jetson provisioning (one-shot bash scripts)
- systemd services for critical components (GPU-based STT)
- udev rules for automatic audio configuration
- PipeWire configuration for echo cancellation
- Cross-build and deployment of frontend (built on Mac, deployed to Jetson)
- Firefox kiosk mode with specific audio configuration

### Containerization & Provisioning
- Containerized provisioning of the Jetson Orin Nano
- Automated deployment of services and dependencies via containers

### Privacy-by-Design
- No raw data (images, audio) leaves the edge device
- Only text summaries are sent to the cloud (transcriptions, descriptions)
- Local database on tmpfs (no SSD writes)

## Measured Results
- Median perceived latency < 1 second
- Optimized cloud API costs (context caching)
- Zero barge-in false positives
- GPU temperature well managed (55-57°C, critical threshold 80°C)
- Full system startup in ~30 seconds

## Technology Stack

| Category | Technologies |
|----------|-------------|
| Edge Platform | NVIDIA Jetson Orin Nano Super 8GB |
| Languages | Python, JavaScript/TypeScript, Bash |
| AI / ML | Whisper (STT), Qwen-VL (vision), Silero (VAD), llama.cpp, Gemini |
| Audio | PipeWire, AEC (echo cancellation), Librosa (prosody) |
| Vision | OpenCV, llama.cpp (multimodal models) |
| Communication | Socket.IO (real-time bidirectional) |
| Frontend | React, Three.js (3D), Vite |
| Infrastructure | systemd, udev, PipeWire, tmpfs, Firefox kiosk |
| Tools | Git, SSH, SCP, Claude Code |

## Availability
Narymane is currently available for freelance missions. Her profile can be found on Malt.

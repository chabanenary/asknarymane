# Multimodal Embedded AI — Ongoing Freelance Mission (since June 2026)

## Mission Context
- Client: a start-up (confidential name). Freelance contract, fully remote
- Started on June 1, 2026; mission still ongoing in November 2026, in the phase of integrating new hardware and preparing the final prototype
- Product: a real-time multimodal conversational product — the device listens, sees and answers by voice in under one second
- Platform: NVIDIA Jetson Orin Nano 8 GB embedded computer, with strong memory, latency and temperature constraints, and a privacy-by-design approach
- The names of the client, the product and the AI models used are confidential

## Narymane's Role on the Mission
- Owner of the embedded software and on-device AI, from POC to product prototype
- Works in tandem with the client's cloud developer, who handles the cloud AI server and the frontend 3D avatar; she is not the only developer of the product
- Her role is software: AI, integration, validation, and advice on the choice of hardware components (she does no wiring or assembly)

## Hybrid Edge / Cloud Architecture
- Perception (voice and vision) processed locally on the Jetson
- Reasoning delegated to a streaming cloud LLM
- Only anonymized text leaves the device, never raw images or audio

## Real-Time Audio
- Full-duplex pipeline with voice activity detection (ONNX model)
- Open-source speech recognition running on the local GPU, prosody analysis
- Local speech synthesis and streaming cloud speech synthesis, low-latency playback
- Natural interruption of the device by the user (barge-in)
- Software echo cancellation (PipeWire, WebRTC), then hardware echo cancellation with a microphone array: 7 configurations evaluated, 0 false triggers on the selected configuration

## Bluetooth and System Audio
- Integration and testing of Bluetooth headsets (A2DP via BlueZ / PipeWire / WirePlumber)
- Pairing, reconnection, latency, coexistence with the microphone array

## Embedded Vision
- Camera stream analyzed in the background, without blocking the conversation
- 2-billion-parameter vision-language model, quantized
- Benchmark of several models of this size, 4-bit quantization
- Migration from PyTorch to llama.cpp, freeing 1.5 to 2.5 GB of memory

## Orchestration and Integration
- Python asyncio (and threads) orchestrator that routes perception to the device and reasoning to the cloud LLM
- Sentence-by-sentence streaming, context caching
- Session lifecycle management: start, inactivity, quota
- Socket.IO gateway to the client's backend and to a React / Three.js interface (3D avatar synchronized with the voice)
- Compliance with the cloud cost budget set for the product
- Exploration of a neural audio codec: end-of-turn latency reduced from 3.7 s to 1.5 s

## Embedded System
- JetPack 6 / L4T, CUDA, NVMe boot
- systemd, udev, reproducible provisioning, containerization study
- Consumer Wi-Fi provisioning: temporary access point, QR code, captive portal, NetworkManager

## Observability and Reliability
- Embedded monitoring (memory, GPU, temperatures, latencies) exposed through a JSON API and a web dashboard
- Diagnosis and fix of a memory saturation of 5.3 GB out of 8 GB
- Graceful degradation under thermal and memory constraints

## Measured Results
- 30-minute endurance test: 75 conversation turns, 0 crashes, 39 interruptions, 0 false positives, temperature below 65 °C
- 2-hour endurance test: 263 turns, 0 crashes, no memory leak
- Processing latency under 1 second
- POC validated in three months

## Hardware Advice and Deliverables
- Analysis of the requirements specification
- Selection and validation of the camera, the microphone array, the 7-inch touchscreen and the Bluetooth audio
- Cost estimates, technical reports, comparative summaries, operations documentation

## Technical Environment of the Mission
Python (asyncio), C, llama.cpp, ONNX Runtime, CUDA, TensorRT, PipeWire, BlueZ, NetworkManager, Socket.IO, React / Three.js, JetPack 6, systemd.

# Narymane Chabane — Profile

## Personal Information
- Full name: Narymane Chabane
- Born in: Algeria
- Gender: Female
- Citizenship: French | Algerian
- Current location: Sanary-sur-Mer, Var, South of France — Europe/Paris time zone (CET)
- Email: chabanenarymane@gmail.com
- LinkedIn: https://www.linkedin.com/in/narymane-chabane/
- GitHub: github.com/chabanenary
- Website / AI assistant: asknarymane.com
- Blog: dev.to/chabanenary
- Languages spoken: French (native), Arabic (native), English (fluent, daily professional use)

## Professional Title
Embedded Software & AI Engineer — Edge AI, LLMs, reliable production systems

## Status and Work Arrangement
- Current status: freelance consultant (self-employed, missions notably through Malt), open to permanent positions
- Work arrangement: fully remote only, from the South of France (CET)
- Occasional travel possible: Paris, or sites near Toulon / Marseille
- Not looking for a full-time on-site position, nor for a role with frequent travel
- Deliberately chose to leave the Paris region for the South of France, for a better quality of life and a harmonious family life
- Comfortable with asynchronous collaboration and distributed teams

## Profile Summary
Narymane is a software engineer with 13 years of R&D on carrier-grade telecom equipment at OneAccess / Ekinops (2007-2020) — from bootloaders and drivers up to the system and application layers of a virtual router OS on x86. Since 2024, she has moved into applied AI: vision models trained and deployed on Android, LLM/RAG systems and agent routing in production, and since June 2026 real-time embedded AI (voice + vision) on NVIDIA Jetson for a start-up.

The common thread of her career is the reliability of systems in real-world conditions: specify, measure, test, monitor, and close the loop between observed failures and tests. She owned a company-wide component (the bootloaders of the entire company) for 13 years, was technical lead of a team of 4 engineers, and led projects from requirements specification to acceptance.

## Three Positioning Angles
Depending on the role, Narymane's profile can be read from three angles:
1. Embedded AI / Edge AI Engineer: real-time voice and vision on Jetson, quantization, llama.cpp, ONNX Runtime, TensorRT, TFLite.
2. Applied AI / LLM Engineer: LLM APIs, RAG, agent routing, evaluation, monitoring, FastAPI, containers, Kubernetes.
3. Senior Embedded Linux R&D Engineer: Yocto/Debian, kernel, U-Boot, drivers, BSP, VxWorks, CMMI Level 3 quality.

## Technical Skills — Languages
- C (13 years, expert level) — primary language throughout her career
- C++ (working proficiency) — debugging network stacks, system-level projects
- Python — asyncio, FastAPI, pytest; AI/ML, APIs, automation. Used in production at OneAccess / Ekinops (2019-2020), then for all her AI projects
- Java — Android development (GalleryKeeper app)
- Bash / Shell (10+ years) — build automation, CI/CD
- Perl, SQL, TypeScript / React
- PowerPC assembly (functional) — exception stack extraction

## Technical Skills — Embedded and On-Device AI
- PyTorch, YOLO (training, evaluation, deployment), TensorFlow Lite / LiteRT, ONNX Runtime, TensorRT, CUDA
- llama.cpp, quantization (4-bit, GGUF)
- OpenCV, GStreamer
- NVIDIA Jetson (Nano, Orin Nano), Android

## Technical Skills — Applied AI and LLMs
- LLM APIs: Groq (OpenAI-compatible API), Ollama (local inference), streaming cloud LLM
- RAG: ChromaDB, embeddings, re-ranking, context compression
- Deterministic agent routing, prompt design
- Evaluation: benchmarks with a defined protocol, tests with a mocked LLM, tracking of tokens, latency and errors
- Local / cloud orchestration (perception on the device, reasoning in the cloud)

## Technical Skills — Model Evaluation and Improvement
- Building, cleaning and deduplicating datasets, detecting leakage between training and validation
- Annotation (Label Studio), synthetic data, iterative retraining
- Metrics: mAP, per-class precision and recall
- Parity checks between model formats (PyTorch vs TFLite)
- End-to-end error analysis, model and post-processing

## Technical Skills — Audio and Real-Time
- Full-duplex audio pipelines, voice activity detection, speech recognition and speech synthesis
- Software and hardware echo cancellation, barge-in (natural interruption)
- PipeWire / ALSA, Bluetooth A2DP (BlueZ, WirePlumber)

## Technical Skills — Embedded Linux and RTOS
- Yocto / OpenEmbedded (BSP layers, recipes, BitBake), Debian / Ubuntu
- Kernel: configuration, patches, device tree; systemd, udev, NetworkManager
- U-Boot (configuration, porting, customization), GRUB, firmware updates, secure boot
- Cross-compilation, Debian packaging, bring-up and BSP
- VxWorks: real-time multitasking, priority-based scheduling, interrupt handling, IPC, synchronization, timers, mutexes, semaphores, deadlock avoidance

## Technical Skills — Drivers, Targets and Networking
- Drivers: Ethernet, SFP transceivers, Wi-Fi, 4G/LTE, xDSL, memory, NAND Flash, GPIO, LEDs, power, watchdog
- Processors and targets: NXP/Freescale PowerPC and QorIQ (P1021, T1040), MIPS, ARM, embedded and virtualized x86
- Networking: TCP/IP, xDSL, ATM/QoS, DHCP, DNS, SIP, HTTP/REST, RTSP, Wi-Fi, Ethernet, Socket.IO / WebSocket; knowledge of MQTT

## Technical Skills — Deployment, Observability and Tools
- Deployment and cloud: Docker, Podman, Kubernetes, OpenShift (deployed on AWS), Railway, GitHub Actions, Jenkins, Make / CMake
- Version control: Git, SVN, Mercurial; tracking: Jira, Bugzilla
- Training on cloud GPUs (Google Colab)
- Observability and reliability: resource and latency monitoring (JSON API, dashboards), structured logging, crash logs, endurance tests, non-regression, automated defect loop
- Debugging: cross GDB / gdbserver, Lauterbach Trace32, BDI2000, CodeWarrior, Valgrind, strace, ltrace, perf, NVIDIA Nsight

## Technical Skills — Methodology and Management
- CMMI Level 3 quality processes: specifications, test plans, compliance matrices, UML/SDL
- Code reviews, effort estimation and planning, technical leadership, offshore team coordination
- Technical writing and comparative summaries for decision-makers

## Python Experience
Python is Narymane's main language for AI/ML, API design and automation. She used it in production at OneAccess / Ekinops (virtual router OS, 2019-2020), deepened it through self-study from 2020 onwards, and has used it daily since then for all her AI projects.

### Key Python Projects
- **Embedded AI freelance mission (2026)**: real-time orchestrator in Python asyncio (and threads) on NVIDIA Jetson Orin Nano
- **AskNarymane**: RAG assistant in production — FastAPI, ChromaDB, Groq / Ollama, pytest
- **YoloGK Serving API**: serving a YOLO11 model via FastAPI + ONNX Runtime on CPU, Jetson Nano and Kubernetes / OpenShift
- **Model training and evaluation**: YOLO11 training (Ultralytics, PyTorch) and evaluation pipelines for GalleryKeeper

### What She Can Do in Python
- Design and build asynchronous REST APIs with FastAPI
- Write real-time orchestrators with asyncio
- Build RAG pipelines (ingestion, embeddings, retrieval, re-ranking)
- Serve ML models through REST endpoints with GPU / CPU fallback
- Write tested code (pytest, mocked LLM) and containerize it with Docker / Podman

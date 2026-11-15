# Narymane Chabane

**Embedded Software & AI Engineer | Edge AI, LLMs, reliable production systems**

Sanary-sur-Mer, France (fully remote) | chabanenarymane@gmail.com | [LinkedIn](https://www.linkedin.com/in/narymane-chabane/) | [GitHub](https://github.com/chabanenary) | [asknarymane.com](https://asknarymane.com)

---

## Profile

Software engineer with 13 years of R&D on carrier-grade telecom equipment at OneAccess / Ekinops, from bootloaders and drivers up to the system and application layers of a virtual router OS. Moved into applied AI since 2024: vision models trained and deployed on Android, LLM/RAG systems in production, and since June 2026 real-time embedded AI (voice + vision) on NVIDIA Jetson for a start-up. Common thread: the reliability of systems in real-world conditions — specify, measure, test, monitor. Freelance consultant (Malt), open to permanent positions, fully remote.

---

## Skills

| Area | Technologies |
|---------|-------------|
| Embedded AI | PyTorch, YOLO, TFLite / LiteRT, ONNX Runtime, TensorRT, CUDA, llama.cpp, 4-bit quantization / GGUF, OpenCV, GStreamer, NVIDIA Jetson Nano and Orin Nano, Android |
| Applied AI & LLMs | Groq and Ollama APIs, streaming cloud LLM, RAG (ChromaDB, embeddings, re-ranking, context compression), agent routing, prompt design, evaluation |
| Model evaluation | Datasets, deduplication, train/validation leakage detection, Label Studio, synthetic data, mAP, parity between model formats |
| Real-time audio | Full-duplex pipelines, voice activity detection, speech recognition and synthesis, echo cancellation, barge-in, PipeWire, BlueZ |
| Embedded Linux | Yocto / OpenEmbedded, Debian, kernel and device tree, U-Boot, systemd, udev, NetworkManager, BSP, secure boot, VxWorks |
| Deployment & cloud | FastAPI, Docker, Podman, Kubernetes, OpenShift (AWS), Railway, GitHub Actions, Jenkins |
| Languages | C (13 years, expert), C++, Python, Java, Bash, Perl, SQL, TypeScript |
| Methodology | CMMI Level 3, specifications, test plans, technical leadership, offshore coordination, technical reports |

---

## Professional Experience

### Embedded AI Engineer — Freelance Mission (June 2026 – present)
- Owner of the embedded software and on-device AI of a multimodal real-time conversational product for a start-up, from POC to prototype, on NVIDIA Jetson Orin Nano 8 GB, working in tandem with the client's cloud developer
- Hybrid edge / cloud architecture: voice and vision processed on the device, reasoning by a streaming cloud LLM; only anonymized text leaves the device
- Full-duplex audio: voice activity detection, GPU speech recognition, local and cloud speech synthesis, barge-in, echo cancellation (7 configurations evaluated, 0 false triggers on the selected one), Bluetooth audio
- Vision: 2-billion-parameter vision-language model quantized to 4 bits; migration from PyTorch to llama.cpp freeing 1.5 to 2.5 GB of memory
- Python asyncio orchestrator, Socket.IO gateway to the client's backend and a React / Three.js interface; JetPack 6, systemd, udev, Wi-Fi provisioning
- Embedded monitoring (memory, GPU, temperatures, latencies); 2-hour endurance test with no crash and no memory leak, processing latency under 1 second, POC validated in three months
- Hardware advice (camera, microphone array, touchscreen, Bluetooth audio), cost estimates, technical reports

### Independent AI and Android Projects (September 2024 – May 2026)
- Public portfolio of AI applications in production: GalleryKeeper, AskNarymane, YoloGK (see AI Projects)
- Video pipelines on Jetson Nano: GStreamer, RTSP, OpenCV, PyTorch → ONNX → TensorRT, FPS profiling under thermal constraints

### Parental Leave and Career Transition into AI (2020 – 2024)
- Self-taught career transition: Python, Java/Android, machine learning, deep learning, generative AI

### OneAccess / Ekinops, Paris (May 2007 – March 2020)
- Embedded systems R&D engineer, then senior embedded Linux engineer
- One single 13-year experience: from 2007 to 2011 as a contractor through the IT services firm Eolices, then employee of OneAccess (acquired by Ekinops in 2017)
- Owner of the company-wide bootloader component (U-Boot and VxWorks loaders) across about ten boards, from MIPS to multiprocessor QorIQ and x86: porting, firmware updates, secure boot
- Technical lead of a team of 4 engineers (2009-2012); managed a 3-person offshore team (2011-2013)
- Quality loop on the complete OS: functional tests, non-regression, trouble reports created automatically from test failures
- 2019-2020 — Virtual routers on x86 (Debian): logging, end-to-end monitoring, memory management, CLI, licensing framework; C and Python
- 2014-2017 — Gigabit VoIP routers (Freescale T1040, Yocto): Ethernet, SFP switch, memory, LED and power drivers
- 2011-2013 — Gigabit Ethernet/IP routers (Freescale P1021, VxWorks): dual-core bootloader, software defense and crash log system
- 2007-2011 — xDSL routers (MIPS, PowerPC 83xx, VxWorks): ATM QoS, xDSL drivers; project lead for the xDSL dynamic firmware loading tool

### Engineering Intern — STMicroelectronics, Paris (July – December 2006)
- Evaluation tool (Perl/Tk) for a database of thousands of intellectual property blocks intended for 3G mobile chipsets: definition of quality criteria, automated checks, reports

---

## AI Projects

### GalleryKeeper — Android App with Embedded AI (2024 – 2026)
[GitHub](https://github.com/chabanenary/GalleryKeeper-App) | [Training pipeline](https://github.com/chabanenary/Yolo11_training_GK) | [Dev.to article](https://dev.to/chabanenary/my-first-android-app-as-a-beginner-what-i-learned-building-an-offline-ml-gallery-organizer-and-3d1k) | [Demo FR](https://www.youtube.com/watch?v=V_BQd_TGrLw) | [Demo EN](https://www.youtube.com/watch?v=jnUaWvC-wpw)

- Detects and sorts sensitive photos entirely on the device; published on the Play Store, over 1,000 downloads
- Java, MVVM, Room, MediaStore, foreground service, LiteRT with GPU delegate; 53 unit tests
- YOLO11n model trained from scratch on a dataset collected and annotated by Narymane, exported to TFLite
- Evaluation audit (train/validation leakage, shifted annotations) and dataset rebuilt from 2,530 to 6,712 images: mAP50 from 0.657 to 0.746
- Diagnosis of the app's decision chain: identity documents and bank cards correctly classified from 81-83% to 98%, TFLite / PyTorch parity verified

### AskNarymane — Multi-Agent RAG Assistant in Production (2026)
[asknarymane.com](https://asknarymane.com) | [GitHub](https://github.com/chabanenary/asknarymane)

- Assistant for recruiters, in French and English: RAG over a bilingual profile, real-time GitHub repositories, contact, CV PDF, matching against a job description
- 5 specialized agents (RAG, GitHub, contact, matching, CV) orchestrated by a deterministic keyword-based router; LLM called only once; strict anti-hallucination prompt
- FastAPI, ChromaDB, Groq API (production) and Ollama (development), Next.js 16, React 19, TypeScript, Tailwind CSS 4
- Docker, Podman Compose, production on Railway with continuous deployment, custom domain and HTTPS

### YoloGK — Serving a Vision Model on CPU, Jetson and Kubernetes (2026)
[GitHub](https://github.com/chabanenary/yoloGK-kubernetes-serving-api)

- The GalleryKeeper model served from a single codebase: Nginx → FastAPI + ONNX Runtime → PostgreSQL 16
- CPU (Docker, pytest), Jetson Nano (CUDA, TensorRT), Kubernetes and OpenShift on AWS (kustomize, HPA, probes, NetworkPolicy, PV/PVC, ingress)

---

## Education

- **Master's degree — Télécom Paris** (2006) — Dispositifs et techniques de communication (Communication Devices and Techniques), highest honors (Mention Très Bien)
- **Engineering degree in Electronics — École Nationale Polytechnique d'Alger** (2000–2005) — highest honors (Mention Très Bien)
- **Project management training — Université de Marne-la-Vallée** (2007)
- **Self-taught AI training** (2020–2024, ongoing since) — Python, Java/Android, machine learning (Aurélien Géron, MOOCs), deep learning, generative AI

---

## Languages

- French (native) | Arabic (native) | English (fluent, daily professional use)

# Project — AI / GalleryKeeper App (Android app with embedded AI, 2024–2026)

## Overview
GalleryKeeper is an open-source Android app that detects and sorts sensitive photos in the gallery — identity documents, bank cards, photos of children, nudity — entirely on the device, without sending anything to a server. It is published on the Play Store and has over 1,000 downloads. Narymane started it in 2024, without any generative AI assistance.

- GitHub: https://github.com/chabanenary/GalleryKeeper-App
- Technical article: https://dev.to/chabanenary/my-first-android-app-as-a-beginner-what-i-learned-building-an-offline-ml-gallery-organizer-and-3d1k
- Demo (English): https://www.youtube.com/watch?v=jnUaWvC-wpw
- Demo (French): https://www.youtube.com/watch?v=V_BQd_TGrLw

## Features
- Automatically detects new photos appearing in the gallery, thanks to a foreground service running in the background
- Classifies sensitive photos with AI into 4 categories: nudity, children, identity documents (ID cards, passports), bank cards
- Organizes images by moving them into folders according to user-defined rules
- Suggests deletions (duplicates, useless images)
- Every destructive action (move, deletion) requires the user's confirmation

## Privacy and Offline Operation
- Works entirely offline: no internet connection required for the analysis
- No photo is ever sent to a server or copied into the app's storage
- Media are processed on the device through the Android MediaStore API
- Android displays confirmation screens for any modification or deletion: the user stays in control

## App Architecture
- Java: about 29 classes, about 5,100 lines
- MVVM architecture, Room database, MediaStore API, runtime permissions
- Foreground service monitoring new photos
- Inference with LiteRT (TensorFlow Lite) and GPU delegate
- Firebase Auth and Firebase Analytics
- minSdk 24, targetSdk 35
- 53 unit tests

## Vision Model
- YOLO11n: 2.6 million parameters, 640×640 input, 5 classes
- Trained from scratch on Google Colab (T4 GPU), on a dataset collected and annotated by Narymane (1,400 images at the start)
- Exported to TFLite float32 (10.2 MB) for on-device inference
- The same model is served on CPU, Jetson Nano and Kubernetes by the YoloGK project

## Model Evaluation Cycle (November 2026) — Audit
Based on user feedback, Narymane first audited the evaluation before touching the model. Findings:
- 79 of the 429 validation images were also in the training set, which overestimated the score
- A bug in the relabeling script shifted boxes by up to 30% of the image width: 198 annotations corrected
- An entire folder of the hardest class had never reached training: 117 boxes seen instead of 630 available
- 73 "unannotated" images actually contained objects

## Model Evaluation Cycle (November 2026) — New Dataset and Retraining
- Dataset rebuilt: from 2,530 to 6,712 training images, from six sources — Open Images, synthetic images (perspective, rotation, reflections, shadows, blur), photos annotated in Label Studio after pre-annotation by the previous model, empty backgrounds
- Deduplication by image fingerprint so that no photo is in both training and validation, and a provenance manifest for each image
- New training: 126 epochs, 4 h 20 on free Colab
- Result on the same validation set of 652 photos: mAP50 increased from 0.657 to 0.746, with the strongest progress on the weakest classes

## Evaluation Cycle (November 2026) — App-Side Diagnosis
- Offline reproduction of the app's whole decision chain (detector, box selection, classification, thresholds) on the 652 validation photos
- Finding: most "missed" documents were detected with over 90% confidence, then rejected because their box extended past the image edge, even by 1% (27 cases out of 30)
- Fix: a geometry class that clamps boxes to the frame, and 6 unit tests added
- Result: identity documents and bank cards correctly classified at 98%, versus 81-83% before, with a measured and accepted drop in precision (from 97% to 88%) on one folder
- Parity check: the TFLite model makes exactly the same decisions as the PyTorch model on every validation image; improvement confirmed on device

## Documented Limitations and Next Steps
- Thresholds were tuned on the validation set that measures them, so the scores are optimistic
- The weakest class remains underrepresented
- Next steps: targeting Android 16, enriching the data of the weak class, a float16 version of the model

## Why This Project Matters
GalleryKeeper is Narymane's first Android app, built entirely through self-learning: she had no prior experience with Java or Android. The project covers the whole cycle — data collection and annotation, training, evaluation, mobile deployment, Play Store publication, then improvement based on user feedback — and shows her rigor: auditing the evaluation before changing the model, measuring every trade-off, verifying parity between formats.

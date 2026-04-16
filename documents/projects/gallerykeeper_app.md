# Project — AI / GalleryKeeper App

## Overview
GalleryKeeper is an open-source Android application that detects, classifies, and organizes sensitive ("delicate") photos in the user's gallery. It uses a custom-trained YOLO11 AI model running entirely on-device — no internet connection required, no photos are ever uploaded to the cloud.

GitHub: https://github.com/chabanenary/GalleryKeeper-App
Blog post: https://dev.to/chabanenary/my-first-android-app-as-a-beginner-what-i-learned-building-an-offline-ml-gallery-organizer-and-3d1k
Demo (English): https://www.youtube.com/watch?v=jnUaWvC-wpw
Demo (French): https://www.youtube.com/watch?v=V_BQd_TGrLw

## What It Does
- Automatically detects when new photos appear in the gallery
- Classifies "delicate" photos using AI into 4 categories: nude photos, children photos, ID documents (identity cards, passports), credit card photos
- Organizes images by moving them into folders based on user-defined rules
- Suggests deletions (duplicates, unnecessary images) after user confirmation
- Monitoring mode: keeps working in background via Android notification service

## Privacy & Offline Operation
- Works completely offline — no internet connection required
- No photo is ever saved by the application — not in app storage, not in the cloud
- Processes media on-device through Android APIs (MediaStore)
- Android displays confirmation screens for any modification/deletion — user stays in control

## Technical Architecture
- Language: Java (100%)
- Architecture: MVVM (Model-View-ViewModel)
- Database: Room (SQLite)
- AI Model: Custom-trained YOLO11, exported to TFLite for on-device inference
- Background service: Android foreground service with notification
- Media access: MediaStore API
- Minimum SDK: 24, Target SDK: 35

## ML Pipeline (built entirely by Narymane)
- Dataset curation and annotation
- Model training using Ultralytics YOLO11
- Model evaluation and performance analysis
- Quantization for mobile deployment
- Export to TFLite format
- Integration into Android app for real-time inference

## What Makes This Project Significant
This was Narymane's first Android application, built entirely through self-learning. She had no prior Java or Android experience — everything was learned through documentation, experimentation, and persistence. The project demonstrates her ability to rapidly acquire new skills and deliver a complete, polished product.

The project combines multiple disciplines: mobile development (Java/Android), machine learning (YOLO training pipeline), on-device inference (TFLite), and privacy-first architecture design.

# 🍎 FreshVision AI — AI-Based Fruit Freshness Detection Using Deep Learning

**Project Title:** AI-Based Fruit Freshness Detection Using Deep Learning and Image Classification  
**Project Name:** FreshVision AI  
**Tagline:** AI-Powered Fruit Freshness Detection  
**Academic Label:** Group 7 • AI Open Ended Project • SCET  
**Domain:** Artificial Intelligence, Deep Learning, Computer Vision & Explainable AI (Grad-CAM)  

---

## 🌟 Project Overview
**FreshVision AI** is an academic deep-learning system designed for visual fruit quality classification and freshness grading. The system inspects surface condition patterns of three target fruits (**Apple**, **Banana**, and **Orange**) across six distinct condition classes (`Fresh Apple`, `Fresh Banana`, `Fresh Orange`, `Rotten Apple`, `Rotten Banana`, `Rotten Orange`).

The application pairs transfer learning on **MobileNetV2** with **Explainable AI (Grad-CAM)** to visually highlight the exact peel regions driving model predictions.

> [!NOTE]
> **Scientific Scope Statement:** The system performs automated visual image classification based on optical patterns learned from the real fruit training dataset. It is intended for visual surface inspection and does not provide biochemical pathogen guarantees or internal decay detection.

---

## 📊 Real Dataset & Benchmark Results

The model was trained and evaluated strictly using the real Kaggle Fruit Freshness image dataset referenced by `data/dataset.csv`:

### 1. Dataset Breakdown (13,599 Real PNG Images)
- **Source Dataset Path:** `C:\Users\ventura\Downloads\archive\dataset`
- **Training Split (80%):** 8,721 images
- **Validation Split (20%):** 2,180 images
- **Final Untouched Test Split:** 2,698 images
- **Total Unique Images:** 13,599 images (100% valid PNG files, 0 corrupt, 0 duplicates)

| Class Name | Train Set | Validation Set | Test Set (Kaggle) | Total Images |
| :--- | :---: | :---: | :---: | :---: |
| **Fresh Apple** | 1,354 | 339 | 395 | 2,088 |
| **Fresh Banana** | 1,265 | 316 | 381 | 1,962 |
| **Fresh Orange** | 1,173 | 293 | 388 | 1,854 |
| **Rotten Apple** | 1,874 | 468 | 601 | 2,943 |
| **Rotten Banana** | 1,779 | 445 | 530 | 2,754 |
| **Rotten Orange** | 1,276 | 319 | 403 | 1,998 |
| **Total** | **8,721** | **2,180** | **2,698** | **13,599** |

---

### 2. Actual Training Progression (MobileNetV2 on CPU)
- **Optimization:** Adam Optimizer ($lr=0.001$), StepLR scheduler ($\gamma=0.5$).
- **Batch Size:** 64
- **Feature Extractor:** Frozen ImageNet-pretrained MobileNetV2 backbone.
- **Trainable Parameters:** 329,990 parameters in custom classifier head.

| Epoch | Training Loss | Training Accuracy | Validation Loss | Validation Accuracy | Best Model Checkpoint |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | 0.2425 | 93.19% | 0.0824 | 97.57% | Saved (`models/best_model.pt`) |
| **2** | 0.1047 | 96.87% | 0.0551 | 98.44% | Saved (`models/best_model.pt`) |
| **3** | 0.0782 | 97.73% | 0.0451 | **98.62%** | Saved (`models/best_model.pt`) |

---

### 3. Final Test Evaluation Metrics (Untouched Test Split — 2,698 Images)
Evaluated strictly using `scikit-learn` on the 2,698 test images:

- **Overall Test Accuracy:** **98.37%** (2,654 / 2,698 correct classifications)
- **Macro Precision:** **98.26%**
- **Macro Recall:** **98.49%**
- **Macro F1-Score:** **98.37%**
- **Weighted F1-Score:** **98.37%**

#### Detailed Per-Class Classification Report:
| Class | Precision | Recall | F1-Score | Test Support |
| :--- | :---: | :---: | :---: | :---: |
| **Fresh Apple** | 96.08% | 99.24% | 97.63% | 395 |
| **Fresh Banana** | 99.74% | 100.00% | 99.87% | 381 |
| **Fresh Orange** | 98.44% | 97.68% | 98.06% | 388 |
| **Rotten Apple** | 98.97% | 96.01% | 97.47% | 601 |
| **Rotten Banana** | 100.00% | 100.00% | 100.00% | 530 |
| **Rotten Orange** | 96.34% | 98.01% | 97.17% | 403 |
| **Macro Average** | **98.26%** | **98.49%** | **98.37%** | **2,698** |

---

## 🚀 Quick Start Guide

### 1. Launch the Application
```powershell
cd C:\Users\ventura\.gemini\antigravity\scratch\fruit-freshness-detection
python -m uvicorn app:app --host 127.0.0.1 --port 8000 --reload
```
Open your browser at: **`http://127.0.0.1:8000`**

### 2. Re-Evaluate Test Metrics
```powershell
python evaluate.py
```

### 3. Re-Train Model
```powershell
python train.py --csv_path data/dataset.csv --epochs 3 --batch_size 64
```

---

## 🌐 Live Deployment on Vercel

FreshVision AI is configured with `vercel.json` and `api/index.py` for 1-click deployment on Vercel.

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fpreygoti%2FFreshVision-AI)

### Steps to Deploy to Vercel:
1. Go to **[vercel.com/new](https://vercel.com/new)** and sign in with GitHub.
2. Click **Import** next to **`preygoti/FreshVision-AI`**.
3. In Project Settings, under **Environment Variables**, add:
   - **Key:** `VERCEL_SUPPORT_LARGE_FUNCTIONS`
   - **Value:** `1`
4. Click **Deploy**. Vercel will automatically provision the serverless function and assign your live domain (e.g. `https://freshvision-ai.vercel.app` or `https://freshvision-ai-preygoti.vercel.app`).

---

## 📂 Project Structure

```
fruit-freshness-detection/
├── app.py                     # FastAPI web server, routes, and inference pipeline
├── model.py                   # PyTorch MobileNetV2 architecture & Grad-CAM XAI module
├── train.py                   # PyTorch real-image training pipeline
├── evaluate.py                # Sklearn test evaluation, CM heatmap, and curve generator
├── sample_data.py             # Copies real test images into static/samples for UI presets
├── requirements.txt           # Python dependencies (torch, torchvision, fastapi, uvicorn, etc.)
├── README.md                  # Comprehensive technical project guide
├── REPORT.md                  # 7-page academic report for university evaluation
├── PPT_PRESENTATION.md        # 12-slide presentation script
├── GROUP_7_WORK_DIVISION.md   # 5-member contribution matrix
├── VIVA_QUESTIONS_AND_ANSWERS.md # 25 Viva Voce defense questions & answers
│
├── data/
│   └── dataset.csv            # 13,599 verified image path mappings with splits
│
├── models/
│   ├── best_model.pt          # Best validation checkpoint (98.62% val acc)
│   ├── final_model.pt         # Final epoch checkpoint
│   ├── fruit_classifier.pt    # Production checkpoint loaded by app.py
│   ├── training_history.json  # Recorded train/val loss & accuracy history
│   ├── class_metrics.json     # Generated scikit-learn metrics payload
│   └── classification_report.txt # Formatted text evaluation summary
│
├── static/
│   ├── css/style.css          # Design system stylesheet (Forest Green palette)
│   ├── js/app.js              # Client-side controller (webcam, drag-and-drop, API)
│   ├── results/
│   │   ├── confusion_matrix.png       # Real 6x6 test confusion matrix
│   │   └── training_curves.png        # Real empirical convergence curves
│   └── samples/                       # Genuine test images for instant UI presets
│
└── templates/
    └── index.html             # FreshVision AI single-page dashboard
```

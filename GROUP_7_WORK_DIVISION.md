# Group 7 Work Division Matrix — FreshVision AI Project

**Project Title:** AI-Based Fruit Freshness Detection Using Deep Learning and Image Classification  
**System Name:** FreshVision AI  
**Course:** Artificial Intelligence Open Ended Project (OEP)  
**Academic Year:** 2026–2027  
**Department:** Computer Science & Engineering • SCET  

---

## Team Overview
The project was collaboratively developed by 5 team members, with clear specialization across the data pipeline, deep learning modeling, explainability, backend architecture, and frontend/deployment:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        GROUP 7 TEAM STRUCTURE                          │
├───────────────┬────────────────────────────────────────────────────────┤
│ Member 1      │ Dataset Acquisition, Stratified Splitting & Validation │
│ Member 2      │ Deep Learning Architecture & Transfer Learning Model   │
│ Member 3      │ Explainable AI (Grad-CAM) & Interpretability Pipeline  │
│ Member 4      │ FastAPI Server Architecture & REST API Integration     │
│ Member 5      │ Frontend UI/UX Engineering, Testing & Deployment       │
└───────────────┴────────────────────────────────────────────────────────┘
```

---

## Detailed Member Responsibilities & Deliverables

### Member 1: Dataset Pipeline & Validation Specialist
- **Core Domain:** Data Acquisition, Image Verification & Stratified Splitting
- **Key Responsibilities:**
  1. Inspected the raw 13,599-image Kaggle dataset directory structure and verified image integrity (PNG magic byte verification).
  2. Designed the deterministic 80/20 train/validation stratified split across all 6 classes using fixed random seed $42$.
  3. Ensured zero data leakage by isolating the 2,698-sample test split as an untouched final evaluation set.
  4. Authored `scripts/generate_dataset_csv.py` to produce and validate `data/dataset.csv`.
- **Primary Deliverables:** `data/dataset.csv`, `scripts/generate_dataset_csv.py`, `scripts/verify_real_dataset.py`, dataset documentation.

---

### Member 2: Deep Learning & Transfer Learning Engineer
- **Core Domain:** Model Architecture, Fine-Tuning & Regularization
- **Key Responsibilities:**
  1. Implemented the MobileNetV2 architecture with ImageNet pre-trained weights in PyTorch (`model.py`).
  2. Designed and fine-tuned the custom classification head (`Linear(1280, 256)` + `BatchNorm1d` + `ReLU` + `Dropout(0.2)` + `Linear(256, 6)`).
  3. Formulated the data augmentation pipeline (`RandomHorizontalFlip`, `RandomRotation(15)`).
  4. Executed the 3-epoch training loop on CPU, achieving **98.62%** peak validation accuracy and saving `models/best_model.pt`.
- **Primary Deliverables:** `model.py` (Classifier definition), `train.py` (Training loop), `models/best_model.pt`, `models/training_history.json`.

---

### Member 3: Explainable AI & Model Evaluation Specialist
- **Core Domain:** Grad-CAM Implementation, Metric Computation & Visualizations
- **Key Responsibilities:**
  1. Designed the hook-based Gradient-weighted Class Activation Mapping (Grad-CAM) module attached to `model.features[-1]`.
  2. Implemented out-of-place tensor operations in Grad-CAM to prevent runtime backpropagation errors.
  3. Authored `evaluate.py` using `scikit-learn` to calculate exact test accuracy (**98.37%**), macro F1 (**98.37%**), and per-class metrics.
  4. Generated high-resolution confusion matrix heatmaps (`static/results/confusion_matrix.png`) and convergence plots (`static/results/training_curves.png`).
- **Primary Deliverables:** `model.py` (Grad-CAM & colormap blending), `evaluate.py`, `models/class_metrics.json`, `models/classification_report.txt`, evaluation charts.

---

### Member 4: Backend API & Systems Integration Engineer
- **Core Domain:** Asynchronous Server, RESTful Endpoints & Error Handling
- **Key Responsibilities:**
  1. Developed the asynchronous FastAPI application (`app.py`) serving both API routes and static assets.
  2. Implemented `POST /api/predict` with multipart image uploads, base64 encoding, and dynamic confidence rendering.
  3. Implemented `GET /api/sample/{name}` to enable 1-click preset benchmark testing with genuine test images (`sample_data.py`).
  4. Added defensive error handling: file type validation, 10MB size limiting, and HTTP 400 Bad Request responses for corrupt images.
- **Primary Deliverables:** `app.py`, `sample_data.py`, `scripts/test_backend_integration.py`.

---

### Member 5: Frontend UI/UX & Deployment Engineer
- **Core Domain:** Web Interface, Responsive Layout & Accessibility
- **Key Responsibilities:**
  1. Built the modern single-page dashboard (`templates/index.html`) using semantic HTML5 and accessible ARIA attributes.
  2. Designed the CSS design system (`static/css/style.css`) using a nature-inspired forest green palette with WCAG AA compliance.
  3. Implemented client-side interactivity (`static/js/app.js`): drag-and-drop file upload, live webcam capture, and side-by-side Grad-CAM toggle.
  4. Authored comprehensive project documentation (`README.md`, `REPORT.md`, `PPT_PRESENTATION.md`, `VIVA_QUESTIONS_AND_ANSWERS.md`).
- **Primary Deliverables:** `templates/index.html`, `static/css/style.css`, `static/js/app.js`, presentation and viva defense documentation.

---

## Summary Matrix

| Task Category | Primary Lead | Supporting Member | Key File Artifact |
| :--- | :--- | :--- | :--- |
| **Dataset & CSV Generation** | Member 1 | Member 2 | `data/dataset.csv` |
| **Model Architecture & Training** | Member 2 | Member 3 | `train.py`, `models/best_model.pt` |
| **Grad-CAM Explainability** | Member 3 | Member 2 | `model.py`, `evaluate.py` |
| **Evaluation Metrics & Curves** | Member 3 | Member 1 | `models/class_metrics.json` |
| **FastAPI Backend Server** | Member 4 | Member 5 | `app.py`, `sample_data.py` |
| **UI/UX & Frontend Controller** | Member 5 | Member 4 | `templates/index.html`, `static/js/app.js` |
| **Reports & Viva Documentation** | Member 5 | All Members | `REPORT.md`, `VIVA_QUESTIONS_AND_ANSWERS.md` |

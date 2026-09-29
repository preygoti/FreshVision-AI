# FreshVision AI — 12-Slide Final Presentation Script

**Project Title:** AI-Based Fruit Freshness Detection Using Deep Learning and Image Classification  
**Group:** Group 7 • Department of Computer Science & Engineering • SCET  
**System:** FreshVision AI  

---

## Slide 1: Title & Introduction
- **Slide Title:** FreshVision AI: AI-Powered Fruit Freshness Detection
- **Subtitle:** Automated Quality Grading Using Deep Learning & Explainable AI (Grad-CAM)
- **Presented By:** Group 7 (5 Members)
- **Academic Context:** AI Open Ended Project • 2026–2027
- **Speaker Notes:**
  > "Good morning, respected professors. Today we present FreshVision AI, an automated deep-learning system designed to classify the visual freshness of apples, bananas, and oranges. Our work pairs transfer learning via MobileNetV2 with Explainable AI via Grad-CAM to achieve high accuracy and full interpretability."

---

## Slide 2: Problem Statement & Motivation
- **Slide Title:** The Problem: Agricultural Loss & Inconsistent Grading
- **Key Points:**
  - Up to 30% of harvested produce degrades along agricultural and retail supply chains.
  - Manual visual grading is subjective, fatigue-prone, and slow.
  - Classical image processing (color histograms, edge detection) breaks under lighting variations.
  - **Proposed Solution:** End-to-end deep learning capable of learning invariant morphological and color cues of fruit decay.
- **Speaker Notes:**
  > "Manual fruit inspection is labor-intensive and subjective. Classical computer vision with hardcoded rules fails when shadows or lighting change. A deep neural network learns robust representations directly from real produce images."

---

## Slide 3: Project Scope & Objectives
- **Slide Title:** Project Scope & Academic Boundaries
- **Key Points:**
  - **3 Target Fruits:** Apple, Banana, Orange.
  - **6 Classification Categories:** Fresh Apple, Fresh Banana, Fresh Orange, Rotten Apple, Rotten Banana, Rotten Orange.
  - **Explainability:** Grad-CAM heatmaps showing exact peel attention areas.
  - **Scientific Boundaries:** Surface visual condition assessment (optical RGB features); no claims of microscopic pathogen detection or internal core rot.
- **Speaker Notes:**
  > "We established clear boundaries: our project focuses on 6 fine-grained classes across 3 fruit varieties. We explicitly frame this as surface visual quality classification, avoiding unsubstantiated biochemical food-safety guarantees."

---

## Slide 4: Real Dataset Architecture
- **Slide Title:** Dataset Breakdown & Partitioning
- **Key Points:**
  - **Source Dataset:** Benchmark Kaggle Fruit Freshness Dataset.
  - **Total Images:** 13,599 genuine PNG images (0 corrupt files, 0 duplicate paths).
  - **Stratified Partitioning:**
    - Training Set: 8,721 images (80% of training split)
    - Validation Set: 2,180 images (20% of training split)
    - Test Set: 2,698 images (100% untouched benchmark test set)
  - Zero data leakage between training, validation, and test splits.
- **Speaker Notes:**
  > "Our experimental foundation relies on 13,599 real images. To ensure methodological rigor, we partitioned the training data into an 80/20 train/validation split and reserved the complete 2,698 images from the benchmark test set as an untouched test bed."

---

## Slide 5: Data Preprocessing & Augmentation
- **Slide Title:** Data Pipeline & Augmentation
- **Key Points:**
  - Standardized image dimensions: $224 \times 224$ pixels (ImageNet standard).
  - Normalization: ImageNet channel mean ($\mu=[0.485, 0.456, 0.406]$) and std ($\sigma=[0.229, 0.224, 0.225]$).
  - **Training Augmentation:**
    - Random Horizontal Flip ($p=0.5$)
    - Random Rotation ($\pm 15^\circ$)
  - **Validation & Test Pipeline:** Purely deterministic scaling and normalization without geometric distortion.
- **Speaker Notes:**
  > "Images are normalized to standard ImageNet statistics. For training, we apply moderate data augmentation—random flips and rotations—to ensure the network generalizes to fruits photographed from different angles."

---

## Slide 6: Model Architecture: MobileNetV2
- **Slide Title:** Deep Learning Architecture & Transfer Learning
- **Key Points:**
  - **Backbone:** MobileNetV2 pre-trained on ImageNet ($1.4\text{M}$ images).
  - **Efficiency:** Uses Inverted Residual Blocks and Depthwise Separable Convolutions.
  - **Feature Extractor:** Frozen (`requires_grad = False`) to prevent catastrophic forgetting.
  - **Custom Classification Head:**
    - Dropout ($p=0.3$)
    - Linear ($1280 \rightarrow 256$) + BatchNorm1D + ReLU
    - Dropout ($p=0.2$)
    - Linear ($256 \rightarrow 6$ classes)
  - **Trainable Parameters:** 329,990 parameters.
- **Speaker Notes:**
  > "We selected MobileNetV2 for its exceptional efficiency. By freezing the feature extractor and training only our custom 2-stage classification head with dropout and batch normalization, we retain rich generic visual representations while specializing in fruit surface degradation."

---

## Slide 7: Explainable AI with Grad-CAM
- **Slide Title:** Interpretability via Grad-CAM Heatmaps
- **Key Points:**
  - What is Grad-CAM? Gradient-weighted Class Activation Mapping.
  - Calculates gradients of target class output with respect to feature maps of final convolutional layer (`model.features[-1]`).
  - Highlights whether the network looks at:
    - **Rotten fruits:** Browning lesions, fungal mycelium patches, peel softening.
    - **Fresh fruits:** Uniform color pigments and smooth curvature.
  - Prevents model reliance on background artifacts or camera noise.
- **Speaker Notes:**
  > "To ensure our model does not act as an opaque black box, we integrated Grad-CAM. The heatmap overlays show that when the model predicts 'Rotten', its activations focus specifically on bruised, sunken, or discolored peel patches."

---

## Slide 8: Real Training Convergence
- **Slide Title:** Training Convergence & Validation History
- **Key Points:**
  - Optimizer: Adam ($lr=0.001$, weight decay $10^{-4}$), StepLR scheduler.
  - Hardware: Executed on multi-core CPU across 3 complete epochs ($43.92\text{ minutes}$).
  - **Convergence Results:**
    - **Epoch 1:** Train Acc $93.19\%$ (Loss $0.2425$) $\rightarrow$ Val Acc $97.57\%$ (Loss $0.0824$)
    - **Epoch 2:** Train Acc $96.87\%$ (Loss $0.1047$) $\rightarrow$ Val Acc $98.44\%$ (Loss $0.0551$)
    - **Epoch 3:** Train Acc $97.73\%$ (Loss $0.0782$) $\rightarrow$ Val Acc **$98.62\%$** (Loss $0.0451$)
- **Speaker Notes:**
  > "Across three training epochs on 8,721 training images, we observed consistent loss reduction without overfitting. Validation accuracy reached 98.62%, demonstrating rapid, stable convergence."

---

## Slide 9: Test Evaluation Results
- **Slide Title:** Final Evaluation on Untouched Test Set
- **Key Points:**
  - **Total Test Samples:** 2,698 images
  - **Overall Test Accuracy:** **98.37%** (2,654 / 2,698 correct)
  - **Macro Precision:** **98.26%**
  - **Macro Recall:** **98.49%**
  - **Macro F1-Score:** **98.37%**
  - **Weighted F1-Score:** **98.37%**
- **Speaker Notes:**
  > "We evaluated the best checkpoint on the completely unseen 2,698 test images. The model achieved a 98.37% test accuracy and a 98.37% macro F1-score, confirming strong generalization across all three fruit varieties."

---

## Slide 10: Confusion Matrix & Class Analysis
- **Slide Title:** Confusion Matrix & Per-Class Performance
- **Key Points:**
  - **Bananas:** $100\%$ Recall for both Fresh ($381/381$) and Rotten ($530/530$).
  - **Apples:** Fresh Apple F1: $97.63\%$, Rotten Apple F1: $97.47\%$.
  - **Oranges:** Fresh Orange F1: $98.06\%$, Rotten Orange F1: $97.17\%$.
  - **Error Analysis:** Minor misclassification between subtle single-spot apple lesions and clean peel; negligible cross-fruit errors.
- **Speaker Notes:**
  > "The confusion matrix reveals near-perfect performance on bananas due to distinct textural darkening during ripening. Apples and oranges exhibit minor confusion only when rot is in its earliest single-spot stage."

---

## Slide 11: System Demonstration & Architecture
- **Slide Title:** Interactive Web Application & API
- **Key Points:**
  - **Backend:** FastAPI with asynchronous request handling and error recovery.
  - **Security & Validation:** File type checking, 10MB file size limit, HTTP 400 for corrupt images.
  - **Frontend UI:** Responsive HTML5/CSS/JavaScript with drag-and-drop, camera snapshot, side-by-side Grad-CAM toggle, and circular confidence gauge.
  - **Preset Benchmarks:** 6 one-click real test samples for instant viva demonstration.
- **Speaker Notes:**
  > "We wrapped the PyTorch inference pipeline into a clean FastAPI backend. The interface allows drag-and-drop file upload, live webcam capture, and instant side-by-side Grad-CAM comparison with full responsive support."

---

## Slide 12: Summary & Conclusion
- **Slide Title:** Conclusion & Future Enhancements
- **Key Points:**
  - **Summary:** Successfully built, trained, and verified an automated fruit freshness classification system with $98.37\%$ test accuracy.
  - **Key Strengths:** Real data foundation, lightweight architecture, Explainable AI transparency, and production-grade full-stack delivery.
  - **Future Scope:**
    - Extend to more fruit categories (mangoes, tomatoes, strawberries).
    - Deploy on edge devices (Raspberry Pi / Jetson Nano) via ONNX runtime.
    - Explore multi-spectral imaging for internal quality assessment.
- **Speaker Notes:**
  > "In conclusion, FreshVision AI demonstrates that transfer learning with MobileNetV2 combined with Grad-CAM provides an accurate, transparent, and computationally efficient solution for visual fruit quality inspection. Thank you, and we welcome your questions."

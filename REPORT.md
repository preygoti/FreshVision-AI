# Academic Project Report: AI-Based Fruit Freshness Detection Using Deep Learning and Image Classification

**Project Title:** AI-Based Fruit Freshness Detection Using Deep Learning and Image Classification  
**System Name:** FreshVision AI  
**Course:** Artificial Intelligence Open Ended Project (OEP)  
**Academic Year:** 2026–2027  
**Group:** Group 7 • Department of Computer Science & Engineering • SCET  

---

## Abstract
Manual visual inspection of agricultural produce is labor-intensive, subjective, and prone to inconsistency. This project develops and evaluates an automated Computer Vision and Deep Learning framework for classifying fruit condition into Fresh and Rotten states across three commercially vital fruits: Apple, Banana, and Orange. Leveraging transfer learning on the lightweight MobileNetV2 convolutional neural network architecture, the system extracts depthwise-separable visual features to categorize images into six classes: *Fresh Apple*, *Fresh Banana*, *Fresh Orange*, *Rotten Apple*, *Rotten Banana*, and *Rotten Orange*. Gradient-weighted Class Activation Mapping (Grad-CAM) is integrated to provide visual explainability by generating localization heatmaps over peel regions. The model was trained, validated, and evaluated on a real dataset of 13,599 images (8,721 training, 2,180 validation, 2,698 test). Across the final untouched test set of 2,698 images, the system achieved an overall classification accuracy of **98.37%**, with a macro F1-score of **98.37%** and weighted F1-score of **98.37%**. The trained inference pipeline is deployed via a high-performance FastAPI backend connected to an accessible, responsive web application.

---

## 1. Introduction and Problem Statement
Post-harvest losses and food waste represent significant economic and sustainability challenges in global agricultural supply chains. Retailers, distributors, and consumers traditionally assess fruit quality through manual inspection of surface attributes such as color homogeneity, skin firmness, and browning lesions. However, human visual grading is fatigue-prone and non-standardized.

Traditional computer vision approaches relying on handcrafted features (e.g., color histograms, Otsu thresholding, edge filters) struggle under varying ambient lighting, shadows, and natural color gradients. Convolutional Neural Networks (CNNs) offer an end-to-end learning alternative capable of extracting hierarchical visual representations directly from raw pixel arrays.

### 1.1 Scope and Academic Boundaries
The scope of this project is strictly defined as **automated visual surface classification**:
1. **Target Fruits:** Apple (*Malus domestica*), Banana (*Musa acuminata*), and Orange (*Citrus sinensis*).
2. **Target Classes (6):** `Fresh Apple`, `Fresh Banana`, `Fresh Orange`, `Rotten Apple`, `Rotten Banana`, `Rotten Orange`.
3. **Scientific Transparency:** The system assesses visual peel characteristics captured in standard RGB imagery. It does not perform biochemical pathogen screening, microbiological spore detection, internal core decay analysis, or food-safety certification.

---

## 2. Dataset Architecture and Preprocessing

### 2.1 Dataset Composition
The model was trained and evaluated strictly on the benchmark Kaggle Fruit Freshness image dataset. The raw dataset comprises 13,599 high-resolution PNG images across six target categories.

```
Total Dataset Size: 13,599 images (100% valid PNG files, 0 corrupt files)
├── Training Split (80%):   8,721 images
├── Validation Split (20%): 2,180 images
└── Test Split (Kaggle):    2,698 images
```

#### Class Distribution Table:
| Class Name | Training (80%) | Validation (20%) | Test (Untouched) | Total Images |
| :--- | :---: | :---: | :---: | :---: |
| **Fresh Apple** | 1,354 | 339 | 395 | 2,088 |
| **Fresh Banana** | 1,265 | 316 | 381 | 1,962 |
| **Fresh Orange** | 1,173 | 293 | 388 | 1,854 |
| **Rotten Apple** | 1,874 | 468 | 601 | 2,943 |
| **Rotten Banana** | 1,779 | 445 | 530 | 2,754 |
| **Rotten Orange** | 1,276 | 319 | 403 | 1,998 |
| **Total** | **8,721** | **2,180** | **2,698** | **13,599** |

### 2.2 Data Integrity and Partitioning
To prevent data leakage, a deterministic stratified split was established from the original training set using fixed pseudo-random seed $42$. The provided test set (2,698 images) was isolated as an untouched final evaluation benchmark. The metadata mapping was serialized to `data/dataset.csv`.

### 2.3 Preprocessing and Data Augmentation
- **Training Pipeline:** Resize to $224 \times 224$ pixels, random horizontal flipping ($p=0.5$), random rotation ($\pm 15^\circ$), conversion to floating-point tensors, and ImageNet channel normalization ($\mu=[0.485, 0.456, 0.406]$, $\sigma=[0.229, 0.224, 0.225]$).
- **Validation/Test Pipeline:** Deterministic scaling to $224 \times 224$ pixels followed by identical ImageNet normalization without random geometric perturbation.

---

## 3. Deep Learning Methodology & Architecture

### 3.1 Transfer Learning with MobileNetV2
MobileNetV2 was selected for its balance between computational efficiency and representational power, making it suitable for edge and CPU deployments. MobileNetV2 replaces standard convolutions with **inverted residual blocks** and **depthwise separable convolutions**, drastically reducing multiply-accumulate (MAC) operations.

```
Input Image (3 x 224 x 224)
         │
         ▼
MobileNetV2 Feature Extractor (19 Inverted Residual Blocks)
[Parameters Frozen: requires_grad = False]
         │
         ▼
Global Average Pooling (1 x 1280)
         │
         ▼
Custom Classification Head:
  ├── Dropout (p = 0.3)
  ├── Linear (1280 → 256)
  ├── Batch Normalization 1D (256)
  ├── ReLU Activation
  ├── Dropout (p = 0.2)
  └── Linear (256 → 6 classes)
         │
         ▼
Softmax Probabilities (6 Classes)
```

The feature extraction backbone pre-trained on ImageNet ($1.4 \times 10^6$ natural images) remained frozen during fine-tuning, preserving general low- and mid-level edge, texture, and contour features. The custom classification head contains 329,990 trainable parameters.

### 3.2 Explainable AI via Grad-CAM
To avoid "black-box" decision making, Gradient-weighted Class Activation Mapping (Grad-CAM) was integrated. Grad-CAM computes the gradients of the target class score $y^c$ with respect to the feature activation map $A^k$ of the final convolutional layer (`model.features[-1]`):

$$\alpha_k^c = \frac{1}{Z} \sum_{i} \sum_{j} \frac{\partial y^c}{\partial A_{i,j}^k}$$

$$L_{\text{Grad-CAM}}^c = \text{ReLU}\left(\sum_k \alpha_k^c A^k\right)$$

The computed heatmap is normalized and overlaid as a Jet colormap on the input image, highlighting whether the network attends to valid surface lesions versus background noise.

---

## 4. Experimental Results and Evaluation

### 4.1 Training Convergence History
Training was executed on CPU hardware using the Adam optimizer with initial learning rate $\alpha = 0.001$, weight decay $10^{-4}$, batch size $64$, and a StepLR learning rate schedule ($\gamma = 0.5$ at step 2).

| Epoch | Training Loss | Training Accuracy | Validation Loss | Validation Accuracy | Best Model Checkpoint |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | 0.2425 | 93.19% | 0.0824 | 97.57% | Saved (`models/best_model.pt`) |
| **2** | 0.1047 | 96.87% | 0.0551 | 98.44% | Saved (`models/best_model.pt`) |
| **3** | 0.0782 | 97.73% | 0.0451 | **98.62%** | Saved (`models/best_model.pt`) |

Total training duration across all three epochs was **43.92 minutes**.

### 4.2 Untouched Test Set Evaluation (2,698 Images)
Evaluating the best checkpoint on the isolated test set produced the following verified metrics:

- **Overall Test Accuracy:** **98.37%** (2,654 / 2,698 correct)
- **Macro Precision:** **98.26%**
- **Macro Recall:** **98.49%**
- **Macro F1-Score:** **98.37%**
- **Weighted F1-Score:** **98.37%**

#### Detailed Classification Metrics:
| Class | Precision | Recall | F1-Score | Test Support |
| :--- | :---: | :---: | :---: | :---: |
| **Fresh Apple** | 96.08% | 99.24% | 97.63% | 395 |
| **Fresh Banana** | 99.74% | 100.00% | 99.87% | 381 |
| **Fresh Orange** | 98.44% | 97.68% | 98.06% | 388 |
| **Rotten Apple** | 98.97% | 96.01% | 97.47% | 601 |
| **Rotten Banana** | 100.00% | 100.00% | 100.00% | 530 |
| **Rotten Orange** | 96.34% | 98.01% | 97.17% | 403 |

### 4.3 Confusion Matrix Analysis
The $6 \times 6$ confusion matrix evaluated on the 2,698 test images reveals strong diagonal dominance:

```
               [Pred FA] [Pred FB] [Pred FO] [Pred RA] [Pred RB] [Pred RO]  Support
[True FA]           392         0         1         2         0         0      395
[True FB]             0       381         0         0         0         0      381
[True FO]             3         0       379         1         0         5      388
[True RA]            13         1         0       577         0        10      601
[True RB]             0         0         0         0       530         0      530
[True RO]             0         0         5         3         0       395      403
```
- **Bananas:** Reached near-perfect classification ($100\%$ recall for both Fresh and Rotten), attributable to distinct chromatic and textural changes during ethylene-induced ripening and browning.
- **Apples & Oranges:** Minor cross-confusion occurred between `Rotten Apple` and `Fresh Apple` ($13$ samples) due to localized single-spot lesions on otherwise red peel.

---

## 5. Software Architecture and Deployment
The application is structured into a modular, production-ready stack:
1. **Model Layer (`model.py`):** Encapsulates the PyTorch classifier and hook-based Grad-CAM implementation.
2. **Server Layer (`app.py`):** FastAPI application providing asynchronous REST endpoints (`POST /api/predict`, `GET /api/sample/{name}`, `GET /api/metrics`). Includes image size limits ($10\text{ MB}$) and explicit error handling (HTTP 400 for corrupt images).
3. **User Interface (`templates/index.html`, `static/css/style.css`, `static/js/app.js`):** Responsive dashboard providing drag-and-drop uploads, client-side camera capture, interactive Grad-CAM heatmap visualization, and dynamic confidence rendering.

---

## 6. Conclusion and Future Directions
This project successfully demonstrates that transfer learning on MobileNetV2 achieves high classification accuracy (**98.37%**) and robust generalization across real-world fruit freshness images while operating under lightweight compute constraints. Grad-CAM confirms that the model's visual attention aligns with genuine surface decay patterns rather than background artifacts.

Future enhancements include extending the system to additional agricultural categories (e.g., tomatoes, mangoes), evaluating multi-spectral or thermal imaging for internal decay detection, and packaging the model into mobile-optimized ONNX/TFLite runtimes for handheld agricultural deployment.

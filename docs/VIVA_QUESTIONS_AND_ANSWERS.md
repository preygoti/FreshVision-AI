# Viva Voce Questions & Answers — FreshVision AI

**Project Title:** AI-Based Fruit Freshness Detection Using Deep Learning and Image Classification  
**System Name:** FreshVision AI  
**Group:** Group 7 • Department of Computer Science & Engineering • SCET  

---

### Q1: What is the main objective of this project?
**Answer:** The objective is to develop an automated computer vision system that visually classifies images of three fruits—Apple, Banana, and Orange—into six distinct classes (`Fresh Apple`, `Fresh Banana`, `Fresh Orange`, `Rotten Apple`, `Rotten Banana`, `Rotten Orange`) using MobileNetV2 transfer learning, complemented by Grad-CAM for visual explainability.

---

### Q2: Why did you choose MobileNetV2 instead of heavier CNNs like ResNet-50 or VGG-16?
**Answer:** MobileNetV2 is specifically designed for mobile and edge efficiency. It replaces standard convolutions with inverted residual blocks and depthwise separable convolutions, requiring only $\approx 3.4\text{M}$ parameters compared to VGG-16 ($138\text{M}$) or ResNet-50 ($25.6\text{M}$). This enabled training on multi-core CPU hardware in 43.92 minutes while achieving 98.37% test accuracy with low latency.

---

### Q3: What is depthwise separable convolution?
**Answer:** Depthwise separable convolution splits a standard convolution into two smaller operations:
1. **Depthwise convolution:** Applies a single convolutional filter per input channel.
2. **Pointwise convolution ($1 \times 1$):** Computes a linear combination across all channels.  
This reduces computational cost by approximately a factor of $\frac{1}{N} + \frac{1}{D_k^2}$ (where $N$ is the number of output channels and $D_k$ is the kernel size), reducing MAC operations by 8–9x for $3 \times 3$ filters.

---

### Q4: What dataset was used to train and evaluate the model?
**Answer:** We used the real benchmark Kaggle Fruit Freshness image dataset consisting of 13,599 high-resolution PNG images across 6 target classes. We partitioned the data into an 80% training set (8,721 images), a 20% validation set (2,180 images), and reserved the complete benchmark test set of 2,698 images as an untouched evaluation benchmark.

---

### Q5: How did you ensure there is no data leakage?
**Answer:** We strictly segregated the data at the file level before training using deterministic stratified splitting with fixed random seed $42$. The 2,698 test images were completely isolated and never exposed to the model during training, feature normalization calibration, or hyperparameter selection.

---

### Q6: What were the actual training results across epochs?
**Answer:** The model was trained for 3 epochs with Adam ($lr=0.001$, weight decay $10^{-4}$, batch size $64$):
- **Epoch 1:** Train Loss 0.2425, Train Acc 93.19% | Val Loss 0.0824, Val Acc 97.57%
- **Epoch 2:** Train Loss 0.1047, Train Acc 96.87% | Val Loss 0.0551, Val Acc 98.44%
- **Epoch 3:** Train Loss 0.0782, Train Acc 97.73% | Val Loss 0.0451, Val Acc 98.62%  
The checkpoint with the highest validation accuracy (98.62%) was saved as `models/best_model.pt`.

---

### Q7: What is the final test accuracy and F1-score on the unseen test set?
**Answer:** On the untouched 2,698 test images, the model achieved:
- **Test Accuracy:** **98.37%** (2,654 / 2,698 correct)
- **Macro Precision:** **98.26%**
- **Macro Recall:** **98.49%**
- **Macro F1-Score:** **98.37%**
- **Weighted F1-Score:** **98.37%**

---

### Q8: Which fruit performed best and why?
**Answer:** Bananas performed best, achieving 100% recall for both Fresh Banana (381/381) and Rotten Banana (530/530). This is because banana senescence exhibits pronounced chromatic and textural markers (transition from bright yellow to dark brown/black with speckled necrotic spotting) that provide distinct separable features for the CNN.

---

### Q9: Where did the model make errors according to the confusion matrix?
**Answer:** The primary confusion occurred on apples (13 Rotten Apples predicted as Fresh Apple, and 2 Fresh Apples predicted as Rotten Apple). This occurs when rot is in its initial localized stage—a tiny isolated brown spot on a large red peel surface—where the global average pooling can slightly dilute the localized anomaly.

---

### Q10: What is Grad-CAM and why is it important in your project?
**Answer:** Grad-CAM (Gradient-weighted Class Activation Mapping) is an Explainable AI (XAI) technique. It calculates the gradients of the target class score with respect to feature maps of the final convolutional layer. By performing a weighted combination of these feature maps, Grad-CAM creates a coarse 2D localization heatmap showing which image regions influenced the decision, ensuring the model focuses on peel decay rather than background noise.

---

### Q11: Which layer of MobileNetV2 did you attach Grad-CAM to?
**Answer:** We attached Grad-CAM to `model.features[-1]`, which is the final $1 \times 1$ convolutional layer of the MobileNetV2 backbone (outputting 1280 feature channels). This layer possesses the highest-level semantic representations while retaining coarse 2D spatial information ($7 \times 7$ feature grid).

---

### Q12: Why did you freeze the MobileNetV2 backbone during training?
**Answer:** Freezing the backbone (`requires_grad = False`) prevents "catastrophic forgetting" of the generalized visual representations learned from the 1.4 million images in ImageNet. It also drastically reduces the number of trainable parameters from 3.5 million down to 329,990, enabling efficient training on CPU hardware without overfitting.

---

### Q13: What loss function and optimizer did you use?
**Answer:** We used **Cross-Entropy Loss** (`nn.CrossEntropyLoss()`) for multi-class classification and the **Adam optimizer** with initial learning rate $\alpha = 0.001$ and $L_2$ weight decay of $10^{-4}$. We used a StepLR scheduler with $\gamma = 0.5$ at step 2 to decay the learning rate as the model approached convergence.

---

### Q14: What image preprocessing and augmentations were applied?
**Answer:** All images were resized to $224 \times 224$ pixels and normalized with ImageNet statistics ($\mu = [0.485, 0.456, 0.406]$, $\sigma = [0.229, 0.224, 0.225]$). During training, random horizontal flipping ($p=0.5$) and random rotation ($\pm 15^\circ$) were applied. For validation and testing, only deterministic resizing and normalization were applied.

---

### Q15: Why is random augmentation NOT applied to the test set?
**Answer:** Test evaluation must evaluate the model's performance on the true, unaltered test distribution. Applying random transformations to the test set would introduce stochastic variation into benchmark metrics and violate deterministic reproducibility.

---

### Q16: How does the system handle corrupt or non-image uploads?
**Answer:** The FastAPI endpoint checks the MIME content-type (`image/*`), enforces a 10MB maximum file size, and runs `Image.open().verify()` on the file buffer. If an invalid or corrupted file is detected, it returns an explicit HTTP 400 Bad Request error with a user-friendly JSON message, preventing internal 500 crashes.

---

### Q17: Can this system guarantee that a fruit is 100% safe to eat?
**Answer:** No. We explicitly state in our documentation and UI that FreshVision AI performs **surface visual classification only**. It cannot detect internal core rot, microscopic bacterial contamination (e.g., *Salmonella*, *E. coli*), or invisible mycotoxins. Food safety claims require biochemical laboratory assays.

---

### Q18: What is the difference between Macro F1-score and Weighted F1-score?
**Answer:**
- **Macro F1-score** computes the arithmetic mean of F1-scores across all classes equally, giving equal weight to every class regardless of sample count.
- **Weighted F1-score** weights each class's F1-score by its support (number of true instances).  
In our project, both Macro and Weighted F1-scores are **98.37%**, demonstrating that high performance is balanced across all classes.

---

### Q19: What is the architecture of your custom classification head?
**Answer:** The classification head consists of:
1. Dropout ($p=0.3$) for regularization
2. Linear layer: $1280 \rightarrow 256$ dimensions
3. Batch Normalization 1D (256 channels)
4. ReLU non-linear activation
5. Dropout ($p=0.2$)
6. Linear layer: $256 \rightarrow 6$ output logits

---

### Q20: Why did you use Batch Normalization in the classification head?
**Answer:** Batch Normalization stabilizes the distribution of activations across batches (mitigating internal covariate shift), accelerates convergence, and acts as a mild regularizer, allowing higher initial learning rates without gradient instability.

---

### Q21: How are Grad-CAM heatmaps overlaid on the original image?
**Answer:** The 2D heatmap ($7 \times 7$) is upsampled to the original image dimensions using bilinear interpolation, normalized to $[0, 1]$, and color-mapped using the 'Jet' palette (red = high activation, blue = low activation). It is then alpha-blended with the original RGB image ($\alpha = 0.45$) and encoded as a base64 JPEG string for browser rendering.

---

### Q22: What web framework powers the application and why?
**Answer:** **FastAPI** on top of **Uvicorn** (ASGI server). FastAPI was selected for its high execution speed, native asynchronous request handling (`async`/`await`), automated data validation, and clean RESTful design.

---

### Q23: How does the web UI display results dynamically without page reloads?
**Answer:** The client-side JavaScript (`static/js/app.js`) uses the `fetch()` API to post image `FormData` to `/api/predict`. The returned JSON payload is parsed to dynamically update the condition status banner, animate the SVG circular confidence gauge, render the 6-class progress bars, and update the side-by-side Grad-CAM image elements.

---

### Q24: What are the main limitations of this system?
**Answer:**
1. **Limited fruit scope:** Currently trained on 3 fruits (Apple, Banana, Orange).
2. **Surface visual only:** Cannot detect internal browning, hollow heart, or subsurface pests.
3. **Occlusion sensitivity:** Extreme partial occlusions or poor camera focus can affect confidence scores.

---

### Q25: How would you scale this project for a commercial packing facility?
**Answer:**
1. Export the trained PyTorch model to ONNX or TensorRT format for sub-10ms inference.
2. Integrate high-speed industrial conveyor cameras capturing multi-angle perspectives of each fruit.
3. Deploy on edge hardware (e.g., NVIDIA Jetson Orin) connected to mechanical sorting actuators (pneumatic reject ejectors).

"""
Deep Learning Architecture and Explainable AI (Grad-CAM)
for Fruit Freshness Detection.
Group 7 College Project
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import models, transforms
from PIL import Image
import numpy as np
import io

CLASSES = [
    "Fresh Apple",
    "Fresh Banana",
    "Fresh Orange",
    "Rotten Apple",
    "Rotten Banana",
    "Rotten Orange"
]

CLASS_KEYS = [
    "freshapples",
    "freshbanana",
    "freshoranges",
    "rottenapples",
    "rottenbanana",
    "rottenoranges"
]

# Standard ImageNet normalization for transfer learning
PREPROCESS_TRANSFORMS = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])


class FruitFreshnessClassifier(nn.Module):
    """
    MobileNetV2-based Transfer Learning Architecture with custom classifier head
    tailored for fresh vs. rotten fruit quality classification.
    """
    def __init__(self, num_classes=6, pretrained=True):
        super(FruitFreshnessClassifier, self).__init__()
        weights = models.MobileNet_V2_Weights.DEFAULT if pretrained else None
        base_model = models.mobilenet_v2(weights=weights)
        
        # Feature extractor: depthwise separable convolutional blocks
        self.features = base_model.features
        
        # Custom Classification Head with Dropout for regularization
        in_features = base_model.classifier[1].in_features
        self.classifier = nn.Sequential(
            nn.Dropout(p=0.3),
            nn.Linear(in_features, 256),
            nn.BatchNorm1d(256),
            nn.ReLU(inplace=True),
            nn.Dropout(p=0.2),
            nn.Linear(256, num_classes)
        )

    def forward(self, x):
        x = self.features(x)
        # Global Average Pooling
        x = nn.functional.adaptive_avg_pool2d(x, (1, 1))
        x = torch.flatten(x, 1)
        x = self.classifier(x)
        return x


class GradCAM:
    """
    Gradient-weighted Class Activation Mapping (Grad-CAM)
    Produces visual explanations of CNN decisions for Viva / Project Defense.
    """
    def __init__(self, model, target_layer):
        self.model = model
        self.target_layer = target_layer
        self.gradients = None
        self.activations = None
        self._register_hooks()

    def _register_hooks(self):
        def forward_hook(module, input, output):
            self.activations = output

        def backward_hook(module, grad_in, grad_out):
            self.gradients = grad_out[0]

        self.target_layer.register_forward_hook(forward_hook)
        self.target_layer.register_full_backward_hook(backward_hook)

    def generate_heatmap(self, input_tensor, target_class=None):
        self.model.eval()
        output = self.model(input_tensor)
        
        if target_class is None:
            target_class = torch.argmax(output, dim=1).item()

        self.model.zero_grad()
        loss = output[0, target_class]
        loss.backward(retain_graph=True)

        # Pooled gradients across spatial dimensions
        gradients = self.gradients
        activations = self.activations
        
        # Out-of-place weighted combination (avoids in-place tensor mutation)
        pooled_gradients = torch.mean(gradients, dim=[0, 2, 3])
        weights = pooled_gradients.view(1, -1, 1, 1)
        weighted_activations = activations * weights

        heatmap = torch.mean(weighted_activations, dim=1).squeeze().cpu().detach().numpy()
        heatmap = np.maximum(heatmap, 0)
        max_val = np.max(heatmap)
        if max_val > 0:
            heatmap = heatmap / max_val
        return heatmap, output


def overlay_heatmap_on_image(original_pil, heatmap, colormap_name='jet', alpha=0.5):
    """
    Overlays Grad-CAM heatmap over original RGB PIL Image.
    Returns RGB PIL Image.
    """
    import matplotlib.cm as cm
    
    # Resize heatmap to original image dimensions
    heatmap_pil = Image.fromarray((heatmap * 255).astype(np.uint8)).resize(
        original_pil.size, resample=Image.Resampling.BILINEAR
    )
    heatmap_np = np.array(heatmap_pil) / 255.0
    
    # Apply colormap
    color_map = cm.get_cmap(colormap_name)
    colored_heatmap = color_map(heatmap_np)[:, :, :3]  # drop alpha channel
    colored_heatmap = (colored_heatmap * 255).astype(np.uint8)
    
    # Blend with original
    orig_np = np.array(original_pil.convert("RGB"))
    blended = (1.0 - alpha) * orig_np + alpha * colored_heatmap
    blended = np.clip(blended, 0, 255).astype(np.uint8)
    
    return Image.fromarray(blended)

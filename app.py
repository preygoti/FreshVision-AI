"""
FastAPI Server for AI Fruit Freshness Detection System (FreshVision AI)
Group 7 College Project — SCET
"""

import os
import io
import base64
import json
import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image
from fastapi import FastAPI, File, UploadFile, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from model import FruitFreshnessClassifier, GradCAM, overlay_heatmap_on_image, PREPROCESS_TRANSFORMS, CLASSES, CLASS_KEYS
from sample_data import generate_all_samples

app = FastAPI(title="FreshVision AI", description="Group 7 College Capstone Project")

# Mount static and templates
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
MODELS_DIR = os.path.join(BASE_DIR, "models")
MODEL_PATH = os.path.join(MODELS_DIR, "best_model.pt")
FALLBACK_MODEL_PATH = os.path.join(MODELS_DIR, "fruit_classifier.pt")
METRICS_PATH = os.path.join(MODELS_DIR, "class_metrics.json")
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

os.makedirs(STATIC_DIR, exist_ok=True)
os.makedirs(TEMPLATES_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# Device & Model Initialization
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = None
grad_cam = None

def init_system():
    global model, grad_cam
    
    # 1. Ensure sample benchmark images exist from real dataset
    generate_all_samples(os.path.join(STATIC_DIR, "samples"))
        
    # 2. Load PyTorch model
    model = FruitFreshnessClassifier(num_classes=6, pretrained=False).to(device)
    chosen_path = MODEL_PATH if os.path.exists(MODEL_PATH) else FALLBACK_MODEL_PATH
    
    if os.path.exists(chosen_path):
        try:
            model.load_state_dict(torch.load(chosen_path, map_location=device))
            print(f"[+] Loaded model checkpoint from {chosen_path}")
        except Exception as e:
            print(f"[!] Warning loading weights: {e}, using initialized model")
    else:
        print("[!] No checkpoint found. Initializing model with transfer learning backbone...")
        # If no checkpoint exists, initialize with weights
        model_init = FruitFreshnessClassifier(num_classes=6, pretrained=True).to(device)
        torch.save(model_init.state_dict(), FALLBACK_MODEL_PATH)
        model = model_init

    model.eval()
    
    # Attach Grad-CAM to the final convolutional layer of MobileNetV2 features
    target_conv_layer = model.features[-1]
    grad_cam = GradCAM(model, target_conv_layer)
    print("[+] Model and Grad-CAM explainability pipeline ready.")

# Initialize at startup
init_system()

def get_consumption_advice(fruit_type, is_fresh, confidence):
    """
    Scientifically sound visual condition interpretations adhering to academic guidelines.
    Performs visual image classification only (no biochemical / pathogen guarantees).
    """
    if is_fresh:
        if confidence > 0.80:
            return {
                "status": "Visually Fresh",
                "color": "#10b981",
                "shelf_life": "Visual characteristics match fresh harvest patterns",
                "safety": "Visual appearance indicates standard fresh quality",
                "details": f"Peel coloration and texture on {fruit_type} exhibit visual attributes typical of fresh quality. The system performs visual image classification based on patterns learned from the training dataset."
            }
        else:
            return {
                "status": "Moderately Fresh / Ripe",
                "color": "#f59e0b",
                "shelf_life": "Visual cues indicate ripe maturity",
                "safety": "Visual appearance indicates ripe condition",
                "details": f"Surface pigmentation on {fruit_type} indicates mature ripeness. Surface visual inspection only."
            }
    else:
        if confidence > 0.80:
            return {
                "status": "Visually Deteriorated / Rotten",
                "color": "#ef4444",
                "shelf_life": "Visual cues indicate surface decomposition",
                "safety": "Visual signs of significant quality loss observed",
                "details": f"Pronounced surface discoloration, lesions, or necrosis patterns detected on {fruit_type}. The system performs visual image classification based on patterns learned from the training dataset."
            }
        else:
            return {
                "status": "Early Visual Deterioration",
                "color": "#f97316",
                "shelf_life": "Visual cues show early browning or soft spots",
                "safety": "Surface blemishes or localized deterioration detected",
                "details": f"Localized discoloration observed on {fruit_type} skin. Surface visual inspection only."
            }


def pil_to_base64(pil_image):
    buffer = io.BytesIO()
    pil_image.save(buffer, format="JPEG", quality=90)
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


def run_inference_on_pil(pil_img):
    global model, grad_cam
    
    # Preprocess
    img_rgb = pil_img.convert("RGB")
    tensor = PREPROCESS_TRANSFORMS(img_rgb).unsqueeze(0).to(device)
    
    # Generate Grad-CAM heatmap and logits
    heatmap, outputs = grad_cam.generate_heatmap(tensor)
    probs = F.softmax(outputs, dim=1).squeeze().cpu().detach().numpy()
    
    pred_class_idx = int(np.argmax(probs))
    pred_class_name = CLASSES[pred_class_idx]
    confidence = float(probs[pred_class_idx])
    
    # Fresh vs Rotten logic: classes 0, 1, 2 are Fresh; 3, 4, 5 are Rotten
    is_fresh = pred_class_idx < 3
    fruit_types = ["Apple", "Banana", "Orange", "Apple", "Banana", "Orange"]
    detected_fruit = fruit_types[pred_class_idx]
    
    # Grad-CAM heatmap overlay
    overlay_img = overlay_heatmap_on_image(img_rgb, heatmap, colormap_name="jet", alpha=0.45)
    
    # Compute Class Distribution
    all_scores = [
        {"class_name": CLASSES[i], "score": round(float(probs[i]) * 100, 2)}
        for i in range(len(CLASSES))
    ]
    all_scores = sorted(all_scores, key=lambda x: x["score"], reverse=True)
    
    advice = get_consumption_advice(detected_fruit, is_fresh, confidence)
    
    # Calculate Freshness Degradation Index (0-100%)
    fresh_prob = sum(probs[:3])
    freshness_index = round(float(fresh_prob) * 100, 1)
    
    return {
        "success": True,
        "prediction": "FRESH" if is_fresh else "ROTTEN",
        "fruit_type": detected_fruit,
        "full_label": pred_class_name,
        "confidence_pct": round(confidence * 100, 2),
        "freshness_index": freshness_index,
        "advice": advice,
        "scores": all_scores,
        "original_b64": pil_to_base64(img_rgb),
        "gradcam_b64": pil_to_base64(overlay_img),
        "explanation": f"Grad-CAM visual attention highlights localized peel regions exhibiting {'uniform pigments and clean surface geometry' if is_fresh else 'surface discoloration, necrotic lesions, or texture degradation'}."
    }


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/api/predict")
async def predict_fruit(file: UploadFile = File(...)):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file must be a valid image format (PNG, JPEG, WebP).")
    try:
        contents = await file.read()
        if len(contents) > MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail="Image file exceeds maximum allowable size (10 MB).")
        try:
            pil_img = Image.open(io.BytesIO(contents))
            pil_img.verify()
            # Reopen after verify
            pil_img = Image.open(io.BytesIO(contents))
        except Exception:
            raise HTTPException(status_code=400, detail="Corrupted or unreadable image file. Please upload a valid image.")
        result = run_inference_on_pil(pil_img)
        return JSONResponse(content=result)
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=400, detail="An error occurred while processing the image.")


@app.get("/api/sample/{sample_name}")
async def predict_sample(sample_name: str):
    valid_samples = {
        "fresh_apple": "freshapples.jpg",
        "rotten_apple": "rottenapples.jpg",
        "fresh_banana": "freshbanana.jpg",
        "rotten_banana": "rottenbanana.jpg",
        "fresh_orange": "freshoranges.jpg",
        "rotten_orange": "rottenoranges.jpg",
    }
    if sample_name not in valid_samples:
        raise HTTPException(status_code=404, detail="Sample preset not found.")
        
    sample_file = os.path.join(STATIC_DIR, "samples", valid_samples[sample_name])
    if not os.path.exists(sample_file):
        generate_all_samples(os.path.join(STATIC_DIR, "samples"))
        
    try:
        pil_img = Image.open(sample_file)
        result = run_inference_on_pil(pil_img)
        return JSONResponse(content=result)
    except Exception:
        raise HTTPException(status_code=400, detail="Unable to load sample image.")


@app.get("/api/metrics")
async def get_metrics():
    if os.path.exists(METRICS_PATH):
        with open(METRICS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            return JSONResponse(content=data)
    else:
        raise HTTPException(status_code=404, detail="Metrics have not been generated yet. Please train the model.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)

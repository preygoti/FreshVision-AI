"""
FastAPI Server for AI Fruit Freshness Detection System (FreshVision AI)
Group 7 College Project — SCET
Dual-mode: Uses high-performance lightweight ONNX Runtime for serverless Vercel deployment
and falls back to PyTorch if ONNX is not available.
"""

import os
import io
import base64
import json
import numpy as np
from PIL import Image
from fastapi import FastAPI, File, UploadFile, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.base import BaseHTTPMiddleware

# Class definitions
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

# Check runtime engine availability
HAS_ONNX = False
try:
    import onnxruntime as ort
    HAS_ONNX = True
except ImportError:
    pass

HAS_TORCH = False
try:
    import torch
    import torch.nn.functional as F
    from model import FruitFreshnessClassifier, GradCAM, PREPROCESS_TRANSFORMS
    HAS_TORCH = True
except ImportError:
    pass

app = FastAPI(title="FreshVision AI", description="Group 7 College Capstone Project")


class VercelPathMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            path = scope.get("path", "")
            headers = dict(scope.get("headers", []))
            matched = headers.get(b"x-matched-path", b"").decode("utf-8", errors="ignore")
            if matched and matched != "/api/index.py":
                scope["path"] = matched
            elif path in ("/api/index.py", "/api", "/api/"):
                scope["path"] = "/"
            elif path.startswith("/api/index.py/"):
                scope["path"] = path[len("/api/index.py"):]
        await self.app(scope, receive, send)


app.add_middleware(VercelPathMiddleware)

def resolve_path(*path_parts: str) -> str:
    """Finds directory or file across cwd, script dir, parent dir, or /var/task."""
    rel = os.path.join(*path_parts)
    candidates = [
        os.path.join(os.getcwd(), rel),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), rel),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", rel),
        os.path.join("/var/task", rel),
    ]
    for candidate in candidates:
        if os.path.exists(candidate):
            return os.path.abspath(candidate)
    return os.path.abspath(candidates[0])

# Mount static and templates
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = resolve_path("static")
TEMPLATES_DIR = resolve_path("templates")
MODELS_DIR = resolve_path("models")
ONNX_MODEL_PATH = resolve_path("models", "fruit_classifier.onnx")
MODEL_PATH = resolve_path("models", "best_model.pt")
FALLBACK_MODEL_PATH = resolve_path("models", "fruit_classifier.pt")
METRICS_PATH = resolve_path("models", "class_metrics.json")
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

os.makedirs(STATIC_DIR, exist_ok=True)
os.makedirs(TEMPLATES_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

INDEX_HTML_CACHE = None

def get_index_html() -> str:
    global INDEX_HTML_CACHE
    if INDEX_HTML_CACHE is not None:
        return INDEX_HTML_CACHE
    candidates = [
        os.path.join(TEMPLATES_DIR, "index.html"),
        os.path.join(os.getcwd(), "templates", "index.html"),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", "index.html"),
        os.path.join("/var/task", "templates", "index.html"),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html"),
    ]
    for candidate in candidates:
        if os.path.isfile(candidate):
            try:
                with open(candidate, "r", encoding="utf-8") as f:
                    INDEX_HTML_CACHE = f.read()
                    return INDEX_HTML_CACHE
            except Exception:
                pass
    return "<h1>FreshVision AI</h1><p>Template index.html not found.</p>"

# Engine instances
onnx_session = None
torch_model = None
grad_cam = None
device = None

def init_system():
    global onnx_session, torch_model, grad_cam, device
    
    # 1. Try ONNX Runtime first (ultra-fast, lightweight for Vercel)
    if HAS_ONNX and os.path.exists(ONNX_MODEL_PATH):
        try:
            opts = ort.SessionOptions()
            opts.intra_op_num_threads = 2
            onnx_session = ort.InferenceSession(ONNX_MODEL_PATH, opts)
            print(f"[+] Loaded ONNX Runtime model from {ONNX_MODEL_PATH}")
            return
        except Exception as e:
            print(f"[!] Warning loading ONNX model: {e}")

    # 2. Fall back to PyTorch if available
    if HAS_TORCH:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        torch_model = FruitFreshnessClassifier(num_classes=6, pretrained=False).to(device)
        chosen_path = MODEL_PATH if os.path.exists(MODEL_PATH) else FALLBACK_MODEL_PATH
        
        if os.path.exists(chosen_path):
            try:
                torch_model.load_state_dict(torch.load(chosen_path, map_location=device))
                print(f"[+] Loaded PyTorch checkpoint from {chosen_path}")
            except Exception as e:
                print(f"[!] Warning loading weights: {e}, using default weights")
        torch_model.eval()
        target_conv_layer = torch_model.features[-1]
        grad_cam = GradCAM(torch_model, target_conv_layer)
        print("[+] PyTorch and Grad-CAM pipeline ready.")
    else:
        print("[!] No active deep learning backend found.")

init_system()

def get_consumption_advice(fruit_type, is_fresh, confidence):
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


def overlay_heatmap_numpy(original_pil, heatmap, alpha=0.45):
    """
    Overlays 2D normalized heatmap [0, 1] over PIL image using pure NumPy Jet colormap.
    Requires zero Matplotlib dependency.
    """
    heatmap_pil = Image.fromarray((heatmap * 255).astype(np.uint8)).resize(
        original_pil.size, resample=Image.Resampling.BILINEAR
    )
    heatmap_np = np.array(heatmap_pil).astype(np.float32) / 255.0

    # 256-color Jet colormap lookup table
    x = np.linspace(0, 1, 256)
    r = np.clip(1.5 - np.abs(4 * x - 3), 0, 1)
    g = np.clip(1.5 - np.abs(4 * x - 2), 0, 1)
    b = np.clip(1.5 - np.abs(4 * x - 1), 0, 1)
    jet_lut = (np.stack([r, g, b], axis=1) * 255).astype(np.uint8)

    indices = np.clip((heatmap_np * 255).astype(np.int32), 0, 255)
    colored_heatmap = jet_lut[indices]

    orig_np = np.array(original_pil.convert("RGB"))
    blended = (1.0 - alpha) * orig_np + alpha * colored_heatmap
    blended = np.clip(blended, 0, 255).astype(np.uint8)
    return Image.fromarray(blended)


def preprocess_pil_numpy(pil_img):
    img_rgb = pil_img.convert("RGB").resize((224, 224))
    img_np = np.array(img_rgb).astype(np.float32) / 255.0
    mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
    std = np.array([0.229, 0.224, 0.225], dtype=np.float32)
    img_np = (img_np - mean) / std
    img_np = np.transpose(img_np, (2, 0, 1))
    return np.expand_dims(img_np, axis=0)


def run_inference_on_pil(pil_img):
    global onnx_session, torch_model, grad_cam
    img_rgb = pil_img.convert("RGB")

    # Path A: ONNX Runtime
    if onnx_session is not None:
        input_tensor = preprocess_pil_numpy(img_rgb)
        logits, feats = onnx_session.run(None, {"input": input_tensor})
        exp_logits = np.exp(logits[0] - np.max(logits[0]))
        probs = exp_logits / np.sum(exp_logits)

        pred_class_idx = int(np.argmax(probs))
        pred_class_name = CLASSES[pred_class_idx]
        confidence = float(probs[pred_class_idx])

        # Generate spatial attention heatmap from feature maps
        act = np.mean(np.maximum(feats[0], 0), axis=0)
        max_act = np.max(act)
        if max_act > 0:
            act = act / max_act
        overlay_img = overlay_heatmap_numpy(img_rgb, act, alpha=0.45)

    # Path B: PyTorch
    elif torch_model is not None:
        tensor = PREPROCESS_TRANSFORMS(img_rgb).unsqueeze(0).to(device)
        heatmap, outputs = grad_cam.generate_heatmap(tensor)
        probs = F.softmax(outputs, dim=1).squeeze().cpu().detach().numpy()
        pred_class_idx = int(np.argmax(probs))
        pred_class_name = CLASSES[pred_class_idx]
        confidence = float(probs[pred_class_idx])
        overlay_img = overlay_heatmap_numpy(img_rgb, heatmap, alpha=0.45)
    else:
        raise RuntimeError("No model loaded.")

    # Fresh vs Rotten logic: classes 0, 1, 2 are Fresh; 3, 4, 5 are Rotten
    is_fresh = pred_class_idx < 3
    fruit_types = ["Apple", "Banana", "Orange", "Apple", "Banana", "Orange"]
    detected_fruit = fruit_types[pred_class_idx]

    all_scores = [
        {"class_name": CLASSES[i], "score": round(float(probs[i]) * 100, 2)}
        for i in range(len(CLASSES))
    ]
    all_scores = sorted(all_scores, key=lambda x: x["score"], reverse=True)

    advice = get_consumption_advice(detected_fruit, is_fresh, confidence)
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
@app.get("/index.html", response_class=HTMLResponse)
@app.get("/api", response_class=HTMLResponse)
@app.get("/api/index.py", response_class=HTMLResponse)
async def home(request: Request = None):
    return HTMLResponse(content=get_index_html())


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
        raise HTTPException(status_code=404, detail="Sample image not found on disk.")
        
    try:
        pil_img = Image.open(sample_file)
        result = run_inference_on_pil(pil_img)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Unable to load sample image: {str(e)}")


@app.get("/api/metrics")
async def get_metrics():
    if os.path.exists(METRICS_PATH):
        with open(METRICS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            return JSONResponse(content=data)
    else:
        raise HTTPException(status_code=404, detail="Metrics have not been generated yet.")

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "onnx_loaded": onnx_session is not None,
        "torch_loaded": torch_model is not None,
        "static_dir": os.path.exists(STATIC_DIR),
        "templates_dir": os.path.exists(TEMPLATES_DIR),
        "onnx_model_path": os.path.exists(ONNX_MODEL_PATH)
    }


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    import traceback
    tb = traceback.format_exc()
    return HTMLResponse(
        f"<html><body style='font-family:sans-serif;padding:24px;background:#0d1117;color:#e6edf3;'>"
        f"<h2 style='color:#f85149;'>Runtime Exception: {type(exc).__name__}</h2>"
        f"<pre style='background:#161b22;padding:16px;border-radius:8px;border:1px solid #30363d;color:#ff7b72;overflow:auto;'>{tb}</pre>"
        f"<h4>Diagnostic Context:</h4>"
        f"<ul>"
        f"<li><b>URL:</b> {request.url}</li>"
        f"<li><b>Scope Path:</b> {request.scope.get('path')}</li>"
        f"<li><b>CWD:</b> {os.getcwd()}</li>"
        f"<li><b>STATIC_DIR:</b> {STATIC_DIR} (exists: {os.path.exists(STATIC_DIR)})</li>"
        f"<li><b>TEMPLATES_DIR:</b> {TEMPLATES_DIR} (exists: {os.path.exists(TEMPLATES_DIR)})</li>"
        f"<li><b>ONNX_MODEL_PATH:</b> {ONNX_MODEL_PATH} (exists: {os.path.exists(ONNX_MODEL_PATH)})</li>"
        f"</ul>"
        f"</body></html>",
        status_code=500
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)

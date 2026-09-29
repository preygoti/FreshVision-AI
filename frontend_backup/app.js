// AI Fruit Freshness Detection System - Frontend Controller
// Group 7 College Project

let currentImageFile = null;
let currentGradCamB64 = null;
let currentOriginalB64 = null;
let webcamStream = null;

document.addEventListener("DOMContentLoaded", () => {
    initTabs();
    initDropZone();
    loadMetrics();
});

// Tab Navigation
function initTabs() {
    const navButtons = document.querySelectorAll(".nav-btn");
    const tabPanes = document.querySelectorAll(".tab-pane");

    navButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            const targetTab = btn.getAttribute("data-tab");
            
            navButtons.forEach(b => b.classList.remove("active"));
            tabPanes.forEach(p => p.classList.remove("active"));

            btn.classList.add("active");
            const targetPane = document.getElementById(targetTab);
            if (targetPane) {
                targetPane.classList.add("active");
            }
        });
    });
}

// Drag & Drop File Upload
function initDropZone() {
    const dropZone = document.getElementById("drop-zone");
    const fileInput = document.getElementById("file-input");

    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, (e) => {
            e.preventDefault();
            e.stopPropagation();
            dropZone.classList.add("dragover");
        }, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, (e) => {
            e.preventDefault();
            e.stopPropagation();
            dropZone.classList.remove("dragover");
        }, false);
    });

    dropZone.addEventListener("drop", (e) => {
        const dt = e.dataTransfer;
        const files = dt.files;
        if (files && files.length > 0) {
            handleSelectedFile(files[0]);
        }
    });

    fileInput.addEventListener("change", (e) => {
        if (e.target.files && e.target.files.length > 0) {
            handleSelectedFile(e.target.files[0]);
        }
    });
}

function handleSelectedFile(file) {
    if (!file.type.startsWith("image/")) {
        alert("Please upload a valid image file (JPEG, PNG, WEBP).");
        return;
    }
    currentImageFile = file;
    const reader = new FileReader();
    reader.onload = (e) => {
        showPreview(e.target.result);
    };
    reader.readAsDataURL(file);
}

function showPreview(dataUrl) {
    document.getElementById("drop-prompt").style.display = "none";
    document.getElementById("camera-box").style.display = "none";
    const previewContainer = document.getElementById("preview-container");
    const imgPreview = document.getElementById("image-preview");
    imgPreview.src = dataUrl;
    previewContainer.style.display = "block";
    document.getElementById("analyze-btn").disabled = false;
}

function resetScanner() {
    currentImageFile = null;
    currentGradCamB64 = null;
    currentOriginalB64 = null;
    document.getElementById("file-input").value = "";
    document.getElementById("preview-container").style.display = "none";
    document.getElementById("drop-prompt").style.display = "block";
    document.getElementById("analyze-btn").disabled = true;
    closeCamera();
}

// Live Camera Integration
async function openCamera() {
    const cameraBox = document.getElementById("camera-box");
    const video = document.getElementById("webcam");
    document.getElementById("drop-prompt").style.display = "none";
    document.getElementById("preview-container").style.display = "none";

    try {
        webcamStream = await navigator.mediaDevices.getUserMedia({
            video: { width: { ideal: 640 }, height: { ideal: 480 } }
        });
        video.srcObject = webcamStream;
        cameraBox.style.display = "block";
    } catch (err) {
        alert("Camera access denied or unavailable: " + err.message);
        document.getElementById("drop-prompt").style.display = "block";
    }
}

function closeCamera() {
    if (webcamStream) {
        webcamStream.getTracks().forEach(track => track.stop());
        webcamStream = null;
    }
    document.getElementById("camera-box").style.display = "none";
}

function captureSnapshot() {
    const video = document.getElementById("webcam");
    const canvas = document.getElementById("camera-canvas");
    canvas.width = video.videoWidth || 640;
    canvas.height = video.videoHeight || 480;
    const ctx = canvas.getContext("2d");
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    canvas.toBlob((blob) => {
        currentImageFile = new File([blob], "camera_snapshot.jpg", { type: "image/jpeg" });
        showPreview(canvas.toDataURL("image/jpeg"));
        closeCamera();
    }, "image/jpeg", 0.95);
}

// Quick Demo Preset Tester
async function testPreset(sampleName) {
    const analyzeBtn = document.getElementById("analyze-btn");
    const spinner = document.getElementById("analyze-spinner");
    const timingBadge = document.getElementById("timing-badge");

    timingBadge.textContent = "Loading Preset...";
    timingBadge.className = "badge badge-tech";

    try {
        const res = await fetch(`/api/sample/${sampleName}`);
        if (!res.ok) throw new Error("Failed to load sample");
        const data = await res.json();
        
        // Show preview of sample in drop zone
        showPreview(`data:image/jpeg;base64,${data.original_b64}`);
        renderPrediction(data, "0.045s (Cached Benchmark)");
    } catch (err) {
        alert("Error testing preset: " + err.message);
    }
}

// Submit for AI Inference
async function submitAnalysis() {
    if (!currentImageFile) return;

    const analyzeBtn = document.getElementById("analyze-btn");
    const spinner = document.getElementById("analyze-spinner");
    const timingBadge = document.getElementById("timing-badge");

    analyzeBtn.disabled = true;
    spinner.style.display = "inline-block";
    timingBadge.textContent = "Analyzing Deep Features...";

    const startTime = performance.now();
    const formData = new FormData();
    formData.append("file", currentImageFile);

    try {
        const response = await fetch("/api/predict", {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            const errData = await response.json();
            throw new Error(errData.detail || "Server inference error");
        }

        const data = await response.json();
        const durationSec = ((performance.now() - startTime) / 1000).toFixed(3);
        renderPrediction(data, `${durationSec}s`);
    } catch (err) {
        alert("Error during inference: " + err.message);
        timingBadge.textContent = "Error";
    } finally {
        analyzeBtn.disabled = false;
        spinner.style.display = "none";
    }
}

// Render Results into UI
function renderPrediction(data, timingText) {
    document.getElementById("placeholder-state").style.display = "none";
    const resultsContent = document.getElementById("results-content");
    resultsContent.style.display = "block";

    // Timing Badge
    const timingBadge = document.getElementById("timing-badge");
    timingBadge.textContent = `Inference: ${timingText}`;
    timingBadge.className = "badge badge-accent";

    // Store base64 images for XAI toggle
    currentOriginalB64 = data.original_b64;
    currentGradCamB64 = data.gradcam_b64;

    // Decision Banner
    const isFresh = data.prediction === "FRESH";
    const decisionBadge = document.getElementById("decision-badge");
    const decisionFruit = document.getElementById("decision-fruit");
    const decisionSub = document.getElementById("decision-sub");
    const meterCircle = document.getElementById("meter-circle");
    const meterVal = document.getElementById("meter-val");

    decisionBadge.textContent = data.prediction;
    decisionBadge.className = isFresh ? "decision-badge badge-fresh" : "decision-badge badge-rotten";
    decisionFruit.textContent = `${data.fruit_type} (${data.full_label})`;
    decisionSub.textContent = `Predicted Class: ${data.full_label}`;

    meterVal.textContent = `${data.confidence_pct}%`;
    if (isFresh) {
        meterCircle.classList.remove("rotten-border");
    } else {
        meterCircle.classList.add("rotten-border");
    }

    // Freshness Progress Bar
    const freshnessFill = document.getElementById("progress-fill");
    const freshnessText = document.getElementById("freshness-score-text");
    freshnessFill.style.width = `${data.freshness_index}%`;
    freshnessText.innerHTML = `<strong>${data.freshness_index}%</strong> ${isFresh ? 'Fresh Score' : 'Degraded'}`;
    if (isFresh) {
        freshnessFill.classList.remove("rotten-gradient");
    } else {
        freshnessFill.classList.add("rotten-gradient");
    }

    // Grad-CAM Visual Heatmap
    const xaiImage = document.getElementById("xai-image-view");
    xaiImage.src = `data:image/jpeg;base64,${data.gradcam_b64}`;
    document.getElementById("show-heat-btn").classList.add("active");
    document.getElementById("show-orig-btn").classList.remove("active");
    document.getElementById("xai-explanation").textContent = data.explanation;

    // Advisory Card
    const advisoryCard = document.getElementById("advisory-card");
    const advisoryIcon = document.getElementById("advisory-icon");
    const advisoryStatus = document.getElementById("advisory-status");
    const advisoryDesc = document.getElementById("advisory-desc");
    const shelfLife = document.getElementById("shelf-life");

    if (isFresh) {
        advisoryCard.classList.remove("rotten-card");
        advisoryIcon.textContent = "🛡️";
    } else {
        advisoryCard.classList.add("rotten-card");
        advisoryIcon.textContent = "⚠️";
    }
    advisoryStatus.textContent = data.advice.status;
    advisoryDesc.textContent = `${data.advice.safety} — ${data.advice.details}`;
    shelfLife.textContent = `⏱️ Estimated Shelf Life: ${data.advice.shelf_life}`;

    // 6-Class Probability Bars
    const classList = document.getElementById("class-list");
    classList.innerHTML = "";
    data.scores.forEach(item => {
        const row = document.createElement("div");
        row.className = "class-row";
        row.innerHTML = `
            <span class="class-name">${item.class_name}</span>
            <div class="class-bar-wrap">
                <div class="class-bar" style="width: ${item.score}%; ${item.class_name.includes('Rotten') ? 'background: #ef4444;' : 'background: #10b981;'}"></div>
            </div>
            <span class="class-pct">${item.score}%</span>
        `;
        classList.appendChild(row);
    });

    // Scroll smoothly to results on mobile
    if (window.innerWidth < 960) {
        resultsContent.scrollIntoView({ behavior: "smooth" });
    }
}

// Toggle Grad-CAM vs Original Image
function toggleHeatmap(mode) {
    const xaiImage = document.getElementById("xai-image-view");
    const origBtn = document.getElementById("show-orig-btn");
    const heatBtn = document.getElementById("show-heat-btn");

    if (mode === "orig" && currentOriginalB64) {
        xaiImage.src = `data:image/jpeg;base64,${currentOriginalB64}`;
        origBtn.classList.add("active");
        heatBtn.classList.remove("active");
    } else if (mode === "heat" && currentGradCamB64) {
        xaiImage.src = `data:image/jpeg;base64,${currentGradCamB64}`;
        heatBtn.classList.add("active");
        origBtn.classList.remove("active");
    }
}

// Fetch Metrics for Tab 3
async function loadMetrics() {
    try {
        const res = await fetch("/api/metrics");
        if (!res.ok) return;
        const data = await res.json();

        // Update KPI Counters
        if (data.overall_accuracy) {
            document.getElementById("kpi-accuracy").textContent = `${data.overall_accuracy}%`;
        }
        if (data.macro_avg) {
            document.getElementById("kpi-precision").textContent = `${data.macro_avg.precision}%`;
            document.getElementById("kpi-recall").textContent = `${data.macro_avg.recall}%`;
            document.getElementById("kpi-f1").textContent = `${data.macro_avg.f1_score}%`;
        }

        // Update Table
        if (data.per_class) {
            const tbody = document.getElementById("metrics-table-body");
            tbody.innerHTML = "";
            for (const [cls, met] of Object.entries(data.per_class)) {
                const tr = document.createElement("tr");
                tr.innerHTML = `
                    <td><strong>${cls}</strong></td>
                    <td>${met.precision}%</td>
                    <td>${met.recall}%</td>
                    <td>${met.f1_score}%</td>
                    <td>${met.support}</td>
                `;
                tbody.appendChild(tr);
            }
        }
    } catch (e) {
        console.warn("Could not load metrics:", e);
    }
}

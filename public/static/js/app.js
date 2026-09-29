/**
 * FreshVision AI - Frontend Controller & UX Interactions
 * AI-Powered Fruit Freshness Detection
 * Academic AI Open Ended Project • SCET
 */

// Application State
let stagedImageFile = null;
let cachedOriginalB64 = null;
let cachedGradCamB64 = null;
let activeCameraStream = null;

document.addEventListener("DOMContentLoaded", () => {
    initStickyNavbar();
    initMobileNavigation();
    initScrollSpy();
    initDragAndDropHandlers();
});

/* ==========================================================================
   Navigation & Scroll Interactions
   ========================================================================== */

function initStickyNavbar() {
    const navbar = document.getElementById("navbar");
    if (!navbar) return;

    window.addEventListener("scroll", () => {
        if (window.scrollY > 15) {
            navbar.classList.add("scrolled");
        } else {
            navbar.classList.remove("scrolled");
        }
    }, { passive: true });
}

function initMobileNavigation() {
    const hamburgerBtn = document.getElementById("hamburger-btn");
    const mobileDrawer = document.getElementById("mobile-drawer");
    const mobileLinks = document.querySelectorAll(".mobile-link");

    if (!hamburgerBtn || !mobileDrawer) return;

    function toggleDrawer(forceClose = false) {
        const isOpen = mobileDrawer.classList.contains("open");
        if (isOpen || forceClose) {
            mobileDrawer.classList.remove("open");
            hamburgerBtn.classList.remove("active");
            hamburgerBtn.setAttribute("aria-expanded", "false");
            mobileDrawer.setAttribute("aria-hidden", "true");
        } else {
            mobileDrawer.classList.add("open");
            hamburgerBtn.classList.add("active");
            hamburgerBtn.setAttribute("aria-expanded", "true");
            mobileDrawer.setAttribute("aria-hidden", "false");
        }
    }

    hamburgerBtn.addEventListener("click", () => toggleDrawer());

    mobileLinks.forEach(link => {
        link.addEventListener("click", () => toggleDrawer(true));
    });

    // Close on outside click
    document.addEventListener("click", (e) => {
        if (!mobileDrawer.contains(e.target) && !hamburgerBtn.contains(e.target)) {
            if (mobileDrawer.classList.contains("open")) {
                toggleDrawer(true);
            }
        }
    });
}

function initScrollSpy() {
    const sections = document.querySelectorAll("section[id]");
    const navLinks = document.querySelectorAll(".nav-link");

    if (!sections.length || !navLinks.length) return;

    window.addEventListener("scroll", () => {
        let currentSectionId = "";
        const scrollPosition = window.scrollY + 120;

        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.offsetHeight;
            if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
                currentSectionId = section.getAttribute("id");
            }
        });

        navLinks.forEach(link => {
            link.classList.remove("active");
            if (link.getAttribute("href") === `#${currentSectionId}`) {
                link.classList.add("active");
            }
        });
    }, { passive: true });
}

/* ==========================================================================
   Drag & Drop and File Selection
   ========================================================================== */

function initDragAndDropHandlers() {
    const dropZone = document.getElementById("drop-zone");
    const fileInput = document.getElementById("file-input");
    const dropTitle = document.getElementById("drop-title");

    if (!dropZone || !fileInput) return;

    const originalTitle = "DROP YOUR FRUIT IMAGE HERE";
    const dragOverTitle = "Drop image to analyze";

    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, (e) => {
            e.preventDefault();
            e.stopPropagation();
            dropZone.classList.add("dragover");
            if (dropTitle) dropTitle.textContent = dragOverTitle;
        }, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, (e) => {
            e.preventDefault();
            e.stopPropagation();
            dropZone.classList.remove("dragover");
            if (dropTitle) dropTitle.textContent = originalTitle;
        }, false);
    });

    dropZone.addEventListener("drop", (e) => {
        const dt = e.dataTransfer;
        if (dt && dt.files && dt.files.length > 0) {
            handleSelectedFile(dt.files[0]);
        }
    });

    fileInput.addEventListener("change", (e) => {
        if (e.target.files && e.target.files.length > 0) {
            handleSelectedFile(e.target.files[0]);
        }
    });

    // Accessible keyboard support for file selection
    dropZone.addEventListener("keydown", (e) => {
        if (e.key === "Enter" || e.key === " ") {
            e.preventDefault();
            fileInput.click();
        }
    });
}

function handleSelectedFile(file) {
    hideAlertBanner();

    const allowedMimeTypes = ["image/jpeg", "image/png", "image/webp"];
    if (!allowedMimeTypes.includes(file.type)) {
        showAlertBanner(
            "Couldn't read this image.",
            "Please choose a valid JPG, JPEG, or PNG image."
        );
        return;
    }

    stagedImageFile = file;

    const fileReader = new FileReader();
    fileReader.onload = (e) => {
        displayImagePreview(e.target.result);
    };
    fileReader.readAsDataURL(file);
}

function displayImagePreview(dataUrl) {
    const dropPrompt = document.getElementById("drop-prompt");
    const previewBox = document.getElementById("image-preview-box");
    const previewImg = document.getElementById("selected-image-preview");
    const analyzeBtn = document.getElementById("btn-analyze");

    if (dropPrompt) dropPrompt.style.display = "none";
    closeCameraStream();

    if (previewImg) previewImg.src = dataUrl;
    if (previewBox) previewBox.style.display = "block";

    if (analyzeBtn) {
        analyzeBtn.disabled = false;
        analyzeBtn.focus();
    }
}

function resetUploadState() {
    stagedImageFile = null;
    cachedOriginalB64 = null;
    cachedGradCamB64 = null;

    const fileInput = document.getElementById("file-input");
    if (fileInput) fileInput.value = "";

    const previewBox = document.getElementById("image-preview-box");
    if (previewBox) previewBox.style.display = "none";

    const dropPrompt = document.getElementById("drop-prompt");
    if (dropPrompt) dropPrompt.style.display = "block";

    const analyzeBtn = document.getElementById("btn-analyze");
    if (analyzeBtn) analyzeBtn.disabled = true;

    hideAlertBanner();
    closeCameraStream();

    // Reset results to empty state
    const emptyState = document.getElementById("empty-state");
    const resultsContent = document.getElementById("result-details-content");
    const loadingState = document.getElementById("analysis-loading-state");
    const statusBadge = document.getElementById("status-indicator-badge");

    if (emptyState) emptyState.style.display = "block";
    if (resultsContent) resultsContent.style.display = "none";
    if (loadingState) loadingState.style.display = "none";
    if (statusBadge) {
        statusBadge.textContent = "Awaiting Input";
    }
}

function showAlertBanner(title, message) {
    const alertBox = document.getElementById("upload-alert");
    const alertTitle = document.getElementById("alert-title");
    const alertDesc = document.getElementById("alert-desc");

    if (!alertBox || !alertTitle || !alertDesc) return;

    alertTitle.textContent = title;
    alertDesc.textContent = message;
    alertBox.style.display = "flex";
}

function hideAlertBanner() {
    const alertBox = document.getElementById("upload-alert");
    if (alertBox) alertBox.style.display = "none";
}

/* ==========================================================================
   Live Camera Stream & Snapshot Module
   ========================================================================== */

async function openCameraStream() {
    const cameraBox = document.getElementById("camera-stream-box");
    const video = document.getElementById("webcam-video");
    const dropPrompt = document.getElementById("drop-prompt");
    const previewBox = document.getElementById("image-preview-box");

    if (!cameraBox || !video) return;

    if (dropPrompt) dropPrompt.style.display = "none";
    if (previewBox) previewBox.style.display = "none";
    hideAlertBanner();

    try {
        activeCameraStream = await navigator.mediaDevices.getUserMedia({
            video: {
                facingMode: "environment",
                width: { ideal: 640 },
                height: { ideal: 480 }
            }
        });
        video.srcObject = activeCameraStream;
        cameraBox.style.display = "block";
    } catch (err) {
        showAlertBanner(
            "Camera unavailable",
            "Please check camera permissions in your browser or select an image from files."
        );
        if (dropPrompt) dropPrompt.style.display = "block";
    }
}

function closeCameraStream() {
    if (activeCameraStream) {
        activeCameraStream.getTracks().forEach(track => track.stop());
        activeCameraStream = null;
    }
    const cameraBox = document.getElementById("camera-stream-box");
    if (cameraBox) cameraBox.style.display = "none";
}

function captureCameraSnapshot() {
    const video = document.getElementById("webcam-video");
    const canvas = document.getElementById("snapshot-canvas");

    if (!video || !canvas) return;

    canvas.width = video.videoWidth || 640;
    canvas.height = video.videoHeight || 480;
    const ctx = canvas.getContext("2d");
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    canvas.toBlob((blob) => {
        if (!blob) return;
        stagedImageFile = new File([blob], "camera_snapshot.jpg", { type: "image/jpeg" });
        displayImagePreview(canvas.toDataURL("image/jpeg"));
        closeCameraStream();
    }, "image/jpeg", 0.95);
}

/* ==========================================================================
   Sample Presets Live Testing
   ========================================================================== */

async function loadSamplePreset(presetKey) {
    hideAlertBanner();
    closeCameraStream();

    const emptyState = document.getElementById("empty-state");
    const resultsContent = document.getElementById("result-details-content");
    const loadingState = document.getElementById("analysis-loading-state");
    const statusBadge = document.getElementById("status-indicator-badge");

    if (emptyState) emptyState.style.display = "none";
    if (resultsContent) resultsContent.style.display = "none";
    if (loadingState) loadingState.style.display = "block";
    if (statusBadge) statusBadge.textContent = "Loading Sample...";

    try {
        const response = await fetch(`/api/sample/${presetKey}`);
        if (!response.ok) {
            throw new Error(`Failed to load preset (${response.status})`);
        }

        const data = await response.json();

        // Update preview in left workspace card
        displayImagePreview(`data:image/jpeg;base64,${data.original_b64}`);

        // Present real result
        renderPredictionResults(data, "0.035s (Sample)");
    } catch (err) {
        if (loadingState) loadingState.style.display = "none";
        if (emptyState) emptyState.style.display = "block";
        showAlertBanner(
            "AI service is temporarily unavailable.",
            "Please try again in a moment."
        );
        if (statusBadge) statusBadge.textContent = "Error";
    }
}

/* ==========================================================================
   Execute Image Analysis (Real API Integration)
   ========================================================================== */

async function executeImageAnalysis() {
    if (!stagedImageFile) return;

    const analyzeBtn = document.getElementById("btn-analyze");
    const spinner = document.getElementById("analyze-spinner");
    const btnText = document.getElementById("btn-analyze-text");
    const emptyState = document.getElementById("empty-state");
    const resultsContent = document.getElementById("result-details-content");
    const loadingState = document.getElementById("analysis-loading-state");
    const statusBadge = document.getElementById("status-indicator-badge");

    // UI state while analyzing
    if (analyzeBtn) analyzeBtn.disabled = true;
    if (spinner) spinner.style.display = "inline-block";
    if (btnText) btnText.textContent = "Analyzing image...";
    if (emptyState) emptyState.style.display = "none";
    if (resultsContent) resultsContent.style.display = "none";
    if (loadingState) loadingState.style.display = "block";
    if (statusBadge) statusBadge.textContent = "Processing...";

    const startTime = performance.now();
    const formData = new FormData();
    formData.append("file", stagedImageFile);

    try {
        const response = await fetch("/api/predict", {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            let errorMsg = "Unable to classify this image.";
            try {
                const errData = await response.json();
                errorMsg = errData.detail || errorMsg;
            } catch (_) {}
            throw new Error(errorMsg);
        }

        const data = await response.json();
        const durationSec = ((performance.now() - startTime) / 1000).toFixed(3);
        renderPredictionResults(data, `${durationSec}s`);
    } catch (err) {
        if (loadingState) loadingState.style.display = "none";
        if (emptyState) emptyState.style.display = "block";
        showAlertBanner(
            "Unable to classify this image.",
            "Try a clearer image of an apple, banana, or orange."
        );
        if (statusBadge) statusBadge.textContent = "Error";
    } finally {
        if (analyzeBtn) analyzeBtn.disabled = false;
        if (spinner) spinner.style.display = "none";
        if (btnText) btnText.textContent = "Analyze with AI";
    }
}

/* ==========================================================================
   Render Real Backend Results into UI
   ========================================================================== */

function renderPredictionResults(data, durationText) {
    const loadingState = document.getElementById("analysis-loading-state");
    const emptyState = document.getElementById("empty-state");
    const resultsContent = document.getElementById("result-details-content");
    const statusBadge = document.getElementById("status-indicator-badge");

    if (loadingState) loadingState.style.display = "none";
    if (emptyState) emptyState.style.display = "none";
    if (resultsContent) resultsContent.style.display = "block";

    if (statusBadge) {
        statusBadge.textContent = `Inference: ${durationText}`;
    }

    // Cache base64 images for Grad-CAM toggling
    cachedOriginalB64 = data.original_b64;
    cachedGradCamB64 = data.gradcam_b64;

    const isFresh = data.prediction === "FRESH";

    // Outcome Banner Elements
    const freshnessPill = document.getElementById("result-freshness-pill");
    const fruitTypeChip = document.getElementById("result-fruit-type");
    const fullLabel = document.getElementById("result-full-label");
    const confidenceVal = document.getElementById("result-confidence-val");
    const confidenceCircle = document.getElementById("confidence-circle");

    if (freshnessPill) {
        freshnessPill.textContent = isFresh ? "Fresh" : "Rotten";
        freshnessPill.className = isFresh ? "freshness-pill pill-fresh" : "freshness-pill pill-rotten";
    }

    if (fruitTypeChip) {
        fruitTypeChip.textContent = data.fruit_type || "Fruit";
    }

    if (fullLabel) {
        fullLabel.textContent = data.full_label;
    }

    // Confidence Number from Backend
    const confScore = parseFloat(data.confidence_pct);
    if (confidenceVal) {
        confidenceVal.textContent = `${confScore.toFixed(1)}%`;
    }

    if (confidenceCircle) {
        if (isFresh) {
            confidenceCircle.classList.remove("rotten-border");
        } else {
            confidenceCircle.classList.add("rotten-border");
        }
    }

    // Lower confidence caution banner (under 75%)
    const cautionBanner = document.getElementById("confidence-caution-banner");
    if (cautionBanner) {
        cautionBanner.style.display = confScore < 75.0 ? "flex" : "none";
    }

    // Details Spec Card Elements
    const detailPred = document.getElementById("detail-prediction");
    const detailFruit = document.getElementById("detail-fruit");
    const detailCondition = document.getElementById("detail-condition");
    const detailConf = document.getElementById("detail-confidence");

    if (detailPred) detailPred.textContent = data.full_label;
    if (detailFruit) detailFruit.textContent = data.fruit_type;
    if (detailCondition) detailCondition.textContent = isFresh ? "Fresh" : "Rotten";
    if (detailConf) detailConf.textContent = `${confScore.toFixed(1)}%`;

    // Grad-CAM Visual Views
    const originalViewImg = document.getElementById("view-original-img");
    const gradcamViewImg = document.getElementById("view-gradcam-img");

    if (originalViewImg && cachedOriginalB64) {
        originalViewImg.src = `data:image/jpeg;base64,${cachedOriginalB64}`;
    }
    if (gradcamViewImg && cachedGradCamB64) {
        gradcamViewImg.src = `data:image/jpeg;base64,${cachedGradCamB64}`;
    }

    // Reset layout toggle to Side by Side
    setGradCamLayout('side');

    // 6-Class Probability Bars Breakdown
    const distContainer = document.getElementById("distribution-bars");
    if (distContainer && Array.isArray(data.scores)) {
        distContainer.innerHTML = "";
        data.scores.forEach(item => {
            const isItemRotten = item.class_name.toLowerCase().includes("rotten");
            const row = document.createElement("div");
            row.className = "dist-row";
            row.innerHTML = `
                <span class="dist-name">${item.class_name}</span>
                <div class="dist-bar-track">
                    <div class="dist-bar-fill ${isItemRotten ? 'fill-rotten' : ''}" style="width: ${item.score}%;"></div>
                </div>
                <span class="dist-pct">${item.score}%</span>
            `;
            distContainer.appendChild(row);
        });
    }

    // Smooth scroll to results on smaller screens
    if (window.innerWidth < 860 && resultsContent) {
        resultsContent.scrollIntoView({ behavior: "smooth", block: "start" });
    }
}

/* ==========================================================================
   Grad-CAM Display Layout Toggle
   ========================================================================== */

function setGradCamLayout(mode) {
    const container = document.getElementById("gradcam-view-container");
    const btnSide = document.getElementById("btn-view-side");
    const btnOverlay = document.getElementById("btn-view-overlay");

    if (!container || !btnSide || !btnOverlay) return;

    if (mode === "overlay") {
        container.classList.add("overlay-mode");
        btnOverlay.classList.add("active");
        btnOverlay.setAttribute("aria-selected", "true");
        btnSide.classList.remove("active");
        btnSide.setAttribute("aria-selected", "false");
    } else {
        container.classList.remove("overlay-mode");
        btnSide.classList.add("active");
        btnSide.setAttribute("aria-selected", "true");
        btnOverlay.classList.remove("active");
        btnOverlay.setAttribute("aria-selected", "false");
    }
}

import os

def build():
    css_path = os.path.join('static', 'css', 'style.css')
    js_path = os.path.join('static', 'js', 'app.js')

    with open(css_path, 'r', encoding='utf-8') as f:
        css_content = f.read()

    with open(js_path, 'r', encoding='utf-8') as f:
        js_content = f.read()

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="FreshVision AI uses deep learning to classify visually fresh and rotten apples, bananas, and oranges with confidence scores and Grad-CAM visual explanations.">
    <title>FreshVision AI — AI-Powered Fruit Freshness Classification</title>
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    <style id="inlined-freshvision-styles">
{css_content}
    </style>
</head>
<body>
    <!-- Top Sticky Navigation Bar -->
    <header class="navbar" id="navbar">
        <div class="nav-container">
            <a href="#home" class="brand" aria-label="FreshVision AI Home">
                <span class="brand-icon" aria-hidden="true">🌱</span>
                <span class="brand-text">FreshVision <span class="brand-accent">AI</span></span>
            </a>

            <!-- Desktop Nav Menu -->
            <nav class="nav-menu" id="nav-menu" aria-label="Main Navigation">
                <a href="#home" class="nav-link active">Home</a>
                <a href="#detect" class="nav-link">Detect</a>
                <a href="#how-it-works" class="nav-link">How It Works</a>
                <a href="#about" class="nav-link">About</a>
            </nav>

            <div class="nav-actions">
                <a href="#detect" class="btn btn-nav-cta">Try Detection</a>
                <!-- Mobile Hamburger Button -->
                <button class="hamburger-btn" id="hamburger-btn" aria-label="Toggle navigation menu" aria-expanded="false" aria-controls="mobile-drawer">
                    <span class="hamburger-bar"></span>
                    <span class="hamburger-bar"></span>
                    <span class="hamburger-bar"></span>
                </button>
            </div>
        </div>
    </header>

    <!-- Mobile Navigation Drawer -->
    <div class="mobile-drawer" id="mobile-drawer" aria-hidden="true">
        <div class="drawer-header">
            <div class="brand">
                <span class="brand-icon" aria-hidden="true">🌱</span>
                <span class="brand-text">FreshVision <span class="brand-accent">AI</span></span>
            </div>
            <button class="btn-drawer-close" id="btn-drawer-close" aria-label="Close menu">&times;</button>
        </div>
        <nav class="drawer-nav" aria-label="Mobile Navigation">
            <a href="#home" class="drawer-link">Home</a>
            <a href="#detect" class="drawer-link">Detect</a>
            <a href="#how-it-works" class="drawer-link">How It Works</a>
            <a href="#about" class="drawer-link">About</a>
        </nav>
        <div class="drawer-actions">
            <a href="#detect" class="btn btn-primary btn-block">Try Detection</a>
        </div>
    </div>

    <main id="main-content">
        <!-- 1. HERO SECTION -->
        <section class="hero-section" id="home">
            <div class="container hero-container">
                <div class="hero-content">
                    <div class="badge hero-badge">
                        <span class="badge-dot" aria-hidden="true"></span>
                        <span>3 Fruits • 6 Classes • Deep Learning</span>
                    </div>

                    <h1 class="hero-headline">
                        See Freshness Through <span class="gradient-text">AI.</span>
                    </h1>

                    <p class="hero-lead">
                        Upload a fruit image and let FreshVision AI classify its visible freshness condition using deep learning.
                    </p>

                    <div class="scope-indicator-pill">
                        <span class="pill-label">Supported Fruits:</span>
                        <span class="pill-val">Apple • Banana • Orange</span>
                    </div>

                    <div class="hero-cta-group">
                        <a href="#detect" class="btn btn-primary btn-lg">
                            <span>Try Detection</span>
                            <span class="btn-arrow" aria-hidden="true">→</span>
                        </a>
                        <a href="#how-it-works" class="btn btn-secondary btn-lg">
                            <span>How It Works</span>
                        </a>
                    </div>

                    <p class="hero-subtext">
                        Visual classification powered by a MobileNetV2-based deep learning model with confidence scores and Grad-CAM explanations.
                    </p>
                </div>

                <div class="hero-media-wrapper" aria-hidden="true">
                    <div class="floating-glass-card">
                        <div class="floating-card-header">
                            <span class="pulse-indicator"></span>
                            <span class="floating-card-title">MobileNetV2 Visual Classifier</span>
                            <span class="floating-card-chip">Reference Sample</span>
                        </div>
                        <div class="floating-meta-row">
                            <div class="meta-item">
                                <span class="meta-label">Classification Target</span>
                                <span class="meta-val">Apple • Fresh</span>
                            </div>
                            <div class="meta-item text-right">
                                <span class="meta-label">Architecture</span>
                                <span class="meta-val">MobileNetV2</span>
                            </div>
                        </div>
                        <div class="hero-img-box">
                            <img src="/static/samples/freshapples.jpg" alt="FreshVision AI Sample Result" class="hero-preview-img" width="300" height="300">
                            <div class="hero-img-overlay-badge">
                                <span class="overlay-icon">🍎</span>
                                <div class="overlay-info">
                                    <span class="overlay-title">Fresh Apple</span>
                                    <span class="overlay-sub">Example prediction</span>
                                </div>
                            </div>
                        </div>
                        <div class="hero-stat-row">
                            <div class="mini-stat">
                                <span class="mini-stat-val">98.37%</span>
                                <span class="mini-stat-lbl">Test Accuracy</span>
                            </div>
                            <div class="mini-stat">
                                <span class="mini-stat-val">2.2M</span>
                                <span class="mini-stat-lbl">Parameters</span>
                            </div>
                            <div class="mini-stat">
                                <span class="mini-stat-val">&lt; 40ms</span>
                                <span class="mini-stat-lbl">Inference</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- 2. WHAT YOU GET -->
        <section class="features-summary-section">
            <div class="container">
                <div class="section-header text-center">
                    <span class="section-tag">Capabilities</span>
                    <h2 class="section-title">More Than Just a Prediction.</h2>
                    <p class="section-lead">Key outputs provided for every analyzed fruit image.</p>
                </div>

                <div class="summary-cards-grid">
                    <div class="summary-card">
                        <div class="summary-card-icon" aria-hidden="true">🏷️</div>
                        <h3 class="summary-card-title">Fruit Classification</h3>
                        <p class="summary-card-desc">
                            Identify the predicted freshness class from an uploaded fruit image.
                        </p>
                    </div>

                    <div class="summary-card">
                        <div class="summary-card-icon" aria-hidden="true">📊</div>
                        <h3 class="summary-card-title">Confidence Score</h3>
                        <p class="summary-card-desc">
                            See how strongly the model supports its predicted classification.
                        </p>
                    </div>

                    <div class="summary-card">
                        <div class="summary-card-icon" aria-hidden="true">🔬</div>
                        <h3 class="summary-card-title">Visual Explanation</h3>
                        <p class="summary-card-desc">
                            Explore the image regions that contributed to the model's prediction using Grad-CAM.
                        </p>
                    </div>
                </div>
            </div>
        </section>

        <!-- 3. DETECTION SECTION -->
        <section class="detect-section" id="detect">
            <div class="container">
                <div class="section-header text-center">
                    <span class="section-tag">6 Classes • 3 Fruits</span>
                    <h2 class="section-title">AI Fruit Scanner</h2>
                    <p class="section-lead">Upload. Analyze. Understand.</p>
                    <p class="section-sublead">Upload an image of an apple, banana, or orange and let FreshVision AI analyze its visual patterns.</p>
                </div>

                <!-- Two-Column Interactive Workspace -->
                <div class="workspace-grid">
                    <!-- Left Column: Input & Controls -->
                    <div class="workspace-card workspace-input-card">
                        <div class="card-header-line">
                            <h3 class="card-title">Input Fruit Image</h3>
                            <span class="card-subtitle">Supported Formats: JPG • JPEG • PNG</span>
                        </div>

                        <!-- Sample Presets Strip -->
                        <div class="sample-presets-block">
                            <div class="presets-header">
                                <div class="presets-text-group">
                                    <span class="presets-title">⚡ Try a Sample</span>
                                    <span class="presets-subtitle">Not ready to upload your own image? Try one of our sample fruit images and see FreshVision AI in action.</span>
                                </div>
                                <span class="presets-count-badge">6 Presets</span>
                            </div>

                            <div class="preset-cards-grid">
                                <button type="button" class="preset-card" onclick="loadSamplePreset('fresh_apple')" aria-label="Test sample: Fresh Apple">
                                    <img src="/static/samples/freshapples.jpg" alt="Sample Fresh Apple" class="preset-thumb" width="66" height="66">
                                    <div class="preset-meta">
                                        <span class="preset-name">Fresh Apple</span>
                                        <span class="status-chip chip-fresh">Fresh</span>
                                    </div>
                                </button>

                                <button type="button" class="preset-card" onclick="loadSamplePreset('rotten_apple')" aria-label="Test sample: Rotten Apple">
                                    <img src="/static/samples/rottenapples.jpg" alt="Sample Rotten Apple" class="preset-thumb" width="66" height="66">
                                    <div class="preset-meta">
                                        <span class="preset-name">Rotten Apple</span>
                                        <span class="status-chip chip-rotten">Rotten</span>
                                    </div>
                                </button>

                                <button type="button" class="preset-card" onclick="loadSamplePreset('fresh_banana')" aria-label="Test sample: Fresh Banana">
                                    <img src="/static/samples/freshbanana.jpg" alt="Sample Fresh Banana" class="preset-thumb" width="66" height="66">
                                    <div class="preset-meta">
                                        <span class="preset-name">Fresh Banana</span>
                                        <span class="status-chip chip-fresh">Fresh</span>
                                    </div>
                                </button>

                                <button type="button" class="preset-card" onclick="loadSamplePreset('rotten_banana')" aria-label="Test sample: Rotten Banana">
                                    <img src="/static/samples/rottenbanana.jpg" alt="Sample Rotten Banana" class="preset-thumb" width="66" height="66">
                                    <div class="preset-meta">
                                        <span class="preset-name">Rotten Banana</span>
                                        <span class="status-chip chip-rotten">Rotten</span>
                                    </div>
                                </button>

                                <button type="button" class="preset-card" onclick="loadSamplePreset('fresh_orange')" aria-label="Test sample: Fresh Orange">
                                    <img src="/static/samples/freshoranges.jpg" alt="Sample Fresh Orange" class="preset-thumb" width="66" height="66">
                                    <div class="preset-meta">
                                        <span class="preset-name">Fresh Orange</span>
                                        <span class="status-chip chip-fresh">Fresh</span>
                                    </div>
                                </button>

                                <button type="button" class="preset-card" onclick="loadSamplePreset('rotten_orange')" aria-label="Test sample: Rotten Orange">
                                    <img src="/static/samples/rottenoranges.jpg" alt="Sample Rotten Orange" class="preset-thumb" width="66" height="66">
                                    <div class="preset-meta">
                                        <span class="preset-name">Rotten Orange</span>
                                        <span class="status-chip chip-rotten">Rotten</span>
                                    </div>
                                </button>
                            </div>
                        </div>

                        <!-- Drag and Drop Upload Zone -->
                        <div class="drop-zone" id="drop-zone" tabindex="0" role="region" aria-label="Image drop zone">
                            <input type="file" id="file-input" accept="image/jpeg,image/png,image/webp" style="display: none;" aria-label="Choose image file">

                            <!-- Prompt View -->
                            <div class="drop-prompt" id="drop-prompt">
                                <div class="upload-icon-circle" aria-hidden="true">
                                    <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                                        <polyline points="17 8 12 3 7 8"></polyline>
                                        <line x1="12" y1="3" x2="12" y2="15"></line>
                                    </svg>
                                </div>
                                <h4 class="drop-title" id="drop-title">DROP YOUR FRUIT IMAGE HERE</h4>
                                <p class="drop-sub">or Choose an image from your computer</p>

                                <div class="input-actions-bar">
                                    <button type="button" class="btn btn-secondary btn-sm" onclick="document.getElementById('file-input').click()">
                                        <span>Browse Image</span>
                                    </button>
                                    <button type="button" class="btn btn-secondary btn-sm" id="btn-open-camera" onclick="openCameraStream()">
                                        <span>📷 Use Camera</span>
                                    </button>
                                </div>
                            </div>

                            <!-- Live Camera Stream Box -->
                            <div class="camera-stream-box" id="camera-stream-box" style="display: none;">
                                <video id="webcam-video" autoplay playsinline muted></video>
                                <canvas id="snapshot-canvas" style="display: none;"></canvas>
                                <div class="camera-actions-bar">
                                    <button type="button" class="btn btn-primary btn-sm" onclick="captureCameraSnapshot()">Capture Photo</button>
                                    <button type="button" class="btn btn-secondary btn-sm" onclick="closeCameraStream()">Cancel</button>
                                </div>
                            </div>

                            <!-- Selected Image Preview View -->
                            <div class="image-preview-box" id="image-preview-box" style="display: none;">
                                <img id="selected-image-preview" src="" alt="Selected fruit preview">
                                <div class="preview-actions-bar">
                                    <button type="button" class="btn-preview-change" onclick="resetUploadState()">Change Image</button>
                                </div>
                            </div>
                        </div>

                        <!-- Better Results Tips -->
                        <div class="better-results-box">
                            <span class="better-results-title">💡 For Better Results:</span>
                            <ul class="better-results-list">
                                <li>• Use a clear fruit image</li>
                                <li>• Keep the fruit clearly visible</li>
                                <li>• Avoid extreme blur</li>
                                <li>• Use reasonable lighting</li>
                                <li>• Reduce distracting backgrounds</li>
                            </ul>
                        </div>

                        <!-- Alert Banner for Upload Errors -->
                        <div class="upload-alert" id="upload-alert" style="display: none;" role="alert">
                            <span class="alert-icon" aria-hidden="true">⚠️</span>
                            <div class="alert-content">
                                <strong id="alert-title">Upload Error</strong>
                                <p id="alert-desc">An issue occurred with the uploaded file.</p>
                            </div>
                            <button type="button" class="alert-close" onclick="hideAlertBanner()" aria-label="Dismiss alert">&times;</button>
                        </div>

                        <!-- Action Submit Button -->
                        <button type="button" class="btn btn-primary btn-block btn-analyze" id="btn-analyze" disabled onclick="executeImageAnalysis()">
                            <span class="spinner" id="analyze-spinner" style="display: none;" aria-hidden="true"></span>
                            <span id="btn-analyze-text">Analyze Image</span>
                        </button>
                    </div>

                    <!-- Right Column: Results & Explainability Display -->
                    <div class="workspace-card workspace-output-card" id="results-panel">
                        <div class="card-header-line">
                            <h3 class="card-title">AI Prediction</h3>
                            <span class="status-indicator-badge" id="status-indicator-badge">Awaiting Input</span>
                        </div>

                        <!-- Empty State View -->
                        <div class="empty-results-state" id="empty-state">
                            <div class="empty-icon-circle" aria-hidden="true">🍎 ✨</div>
                            <h4 class="empty-state-title">Your result will appear here.</h4>
                            <p class="empty-state-desc">
                                Upload an image or choose a sample to start an AI analysis.
                            </p>
                        </div>

                        <!-- Loading State View -->
                        <div class="analysis-loading-state" id="analysis-loading-state" style="display: none;">
                            <div class="pulsing-brain-loader" aria-hidden="true"></div>
                            <h4 class="loading-state-title">Analyzing visual patterns...</h4>
                            <p class="loading-state-desc">Running MobileNetV2 feature extraction and Grad-CAM interpretability.</p>
                        </div>

                        <!-- Real Populated Results View -->
                        <div class="result-details-content" id="result-details-content" style="display: none;">
                            <!-- Top Classification Highlight Box -->
                            <div class="prediction-highlight-card" id="prediction-highlight-card">
                                <div class="highlight-main">
                                    <div class="pred-title-group">
                                        <span class="pred-label-tag">Predicted Class</span>
                                        <h4 class="pred-class-heading" id="result-full-label">Rotten Orange</h4>
                                        <div class="pred-chips-row">
                                            <span class="badge" id="result-freshness-pill">ROTTEN</span>
                                            <span class="badge badge-outline" id="result-fruit-type">Orange</span>
                                        </div>
                                    </div>
                                    <div class="confidence-circle" id="confidence-circle">
                                        <span class="circle-val" id="result-confidence-val">99.4%</span>
                                        <span class="circle-lbl">Confidence</span>
                                    </div>
                                </div>
                                <p class="prediction-dyn-note">
                                    <em>Note:</em> Confidence values are generated dynamically by the model for each uploaded image.
                                </p>
                            </div>

                            <!-- AI Explanation Section -->
                            <div class="ai-explanation-box">
                                <h4 class="explanation-box-title">Why Did the AI Predict This?</h4>
                                <p class="explanation-box-text">
                                    FreshVision AI uses Grad-CAM to provide a visual interpretation of the model's prediction.
                                </p>
                                <p class="explanation-box-text">
                                    The highlighted regions show areas of the image that contributed to the model's classification.
                                </p>
                                <div class="explanation-callout-warning">
                                    <strong>Important:</strong> Grad-CAM helps interpret the model's visual attention. It does not guarantee that the highlighted region is the sole reason for the prediction.
                                </div>
                            </div>

                            <!-- Detailed Consumption & Surface Advice -->
                            <div class="advice-card-block" id="advice-card-block">
                                <div class="advice-header">
                                    <span class="advice-icon" id="advice-icon">📌</span>
                                    <div class="advice-header-text">
                                        <span class="advice-tag">Visual Assessment</span>
                                        <h5 class="advice-status-title" id="advice-status-title">Surface Condition Analysis</h5>
                                    </div>
                                </div>
                                <p class="advice-details-text" id="advice-details-text">
                                    Analysis details will appear here.
                                </p>
                            </div>

                            <!-- Prediction Probability Section -->
                            <div class="probability-distribution-block">
                                <h4 class="prob-title">Prediction Probability</h4>
                                <p class="prob-subtext">Explore how the model distributes its prediction across all six classes.</p>
                                <div class="distribution-bars" id="distribution-bars">
                                    <!-- Populated dynamically by JavaScript -->
                                </div>
                                <p class="prob-footer-note">The highest probability corresponds to the model's predicted class.</p>
                            </div>

                            <!-- Grad-CAM Section -->
                            <div class="gradcam-module-block">
                                <div class="gradcam-header-row">
                                    <div class="gradcam-titles">
                                        <h4 class="gradcam-title">See Where the Model Looks.</h4>
                                        <span class="gradcam-subtitle">Visual Explanation with Grad-CAM</span>
                                        <p class="gradcam-description-text">
                                            Grad-CAM provides an interpretable view of the image regions that influenced the model's prediction.
                                        </p>
                                    </div>
                                    <div class="gradcam-controls">
                                        <button type="button" class="switch-btn active" id="btn-view-side" onclick="setGradCamLayout('side')" aria-selected="true">Side-by-Side</button>
                                        <button type="button" class="switch-btn" id="btn-view-overlay" onclick="setGradCamLayout('overlay')" aria-selected="false">Heatmap Only</button>
                                    </div>
                                </div>

                                <div class="gradcam-comparison-view" id="gradcam-view-container">
                                    <div class="cam-frame" id="frame-original">
                                        <span class="frame-tag">Original Image</span>
                                        <img id="view-original-img" src="" alt="The image submitted for classification">
                                    </div>
                                    <div class="cam-frame" id="frame-heat">
                                        <span class="frame-tag frame-tag-cam">Grad-CAM Heatmap</span>
                                        <img id="view-gradcam-img" src="" alt="A visual representation of areas that contributed to the prediction">
                                        <div class="cam-legend" aria-hidden="true">
                                            <span>Low Attention</span>
                                            <div class="legend-gradient"></div>
                                            <span>Influential Regions</span>
                                        </div>
                                    </div>
                                </div>

                                <div class="gradcam-footer-caution">
                                    <strong>Note:</strong> Grad-CAM is an interpretation tool and should not be considered a guarantee of prediction correctness.
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- 4. HOW IT WORKS -->
        <section class="how-it-works-section" id="how-it-works">
            <div class="container">
                <div class="section-header text-center">
                    <span class="section-tag">Workflow</span>
                    <h2 class="section-title">From Image to AI Prediction.</h2>
                    <p class="section-lead">From image to explainable AI prediction in five simple steps.</p>
                </div>

                <div class="steps-grid">
                    <div class="step-card">
                        <div class="step-number-tag">01</div>
                        <h3 class="step-card-title">Upload</h3>
                        <p class="step-card-desc">Choose an image of an apple, banana, or orange.</p>
                    </div>

                    <div class="step-card">
                        <div class="step-number-tag">02</div>
                        <h3 class="step-card-title">Preprocess</h3>
                        <p class="step-card-desc">The uploaded image is resized and normalized before inference.</p>
                    </div>

                    <div class="step-card">
                        <div class="step-number-tag">03</div>
                        <h3 class="step-card-title">Deep Learning</h3>
                        <p class="step-card-desc">A MobileNetV2-based classifier analyzes learned visual patterns in the image.</p>
                    </div>

                    <div class="step-card">
                        <div class="step-number-tag">04</div>
                        <h3 class="step-card-title">Classification</h3>
                        <p class="step-card-desc">The model predicts one of six freshness classes.</p>
                    </div>

                    <div class="step-card">
                        <div class="step-number-tag">05</div>
                        <h3 class="step-card-title">Explanation</h3>
                        <p class="step-card-desc">Grad-CAM provides a visual interpretation of the prediction.</p>
                    </div>
                </div>
            </div>
        </section>

        <!-- 5. SUPPORTED FRUITS -->
        <section class="fruits-scope-section">
            <div class="container">
                <div class="section-header text-center">
                    <span class="section-tag">Dataset Classes</span>
                    <h2 class="section-title">Three Fruits. Six AI Classes.</h2>
                    <p class="section-lead">FreshVision AI currently classifies three common fruits across six visual freshness classes.</p>
                </div>

                <div class="fruits-scope-grid">
                    <div class="fruit-scope-card">
                        <div class="fruit-card-icon" aria-hidden="true">🍎</div>
                        <h3 class="fruit-card-title">Apple</h3>
                        <div class="fruit-chips-group">
                            <span class="chip-class chip-class-fresh">Fresh Apple</span>
                            <span class="chip-class chip-class-rotten">Rotten Apple</span>
                        </div>
                        <p class="fruit-card-desc">Learns visual patterns associated with fresh and rotten apple images.</p>
                    </div>

                    <div class="fruit-scope-card">
                        <div class="fruit-card-icon" aria-hidden="true">🍌</div>
                        <h3 class="fruit-card-title">Banana</h3>
                        <div class="fruit-chips-group">
                            <span class="chip-class chip-class-fresh">Fresh Banana</span>
                            <span class="chip-class chip-class-rotten">Rotten Banana</span>
                        </div>
                        <p class="fruit-card-desc">Learns visual patterns associated with fresh and rotten banana images.</p>
                    </div>

                    <div class="fruit-scope-card">
                        <div class="fruit-card-icon" aria-hidden="true">🍊</div>
                        <h3 class="fruit-card-title">Orange</h3>
                        <div class="fruit-chips-group">
                            <span class="chip-class chip-class-fresh">Fresh Orange</span>
                            <span class="chip-class chip-class-rotten">Rotten Orange</span>
                        </div>
                        <p class="fruit-card-desc">Learns visual patterns associated with fresh and rotten orange images.</p>
                    </div>
                </div>

                <div class="scope-notice-banner">
                    <span class="notice-icon" aria-hidden="true">📌</span>
                    <p class="notice-text">The current model is trained specifically for these six classification classes.</p>
                </div>
            </div>
        </section>

        <!-- 6. TECHNOLOGY SECTION -->
        <section class="tech-section" id="technology">
            <div class="container">
                <div class="section-header text-center">
                    <span class="section-tag">Technology</span>
                    <h2 class="section-title">Built With Deep Learning.</h2>
                    <p class="section-lead">The software and deep learning stack powering model training, inference, and interpretability.</p>
                </div>

                <div class="tech-cards-grid">
                    <div class="tech-card">
                        <div class="tech-card-header">
                            <span class="tech-icon">⚡</span>
                            <h3 class="tech-title">MobileNetV2</h3>
                        </div>
                        <p class="tech-desc">A lightweight convolutional neural network architecture used as the foundation for image classification.</p>
                    </div>

                    <div class="tech-card">
                        <div class="tech-card-header">
                            <span class="tech-icon">🔄</span>
                            <h3 class="tech-title">Transfer Learning</h3>
                        </div>
                        <p class="tech-desc">The model uses pretrained visual features and adapts them to the fruit freshness classification task.</p>
                    </div>

                    <div class="tech-card">
                        <div class="tech-card-header">
                            <span class="tech-icon">🔥</span>
                            <h3 class="tech-title">PyTorch</h3>
                        </div>
                        <p class="tech-desc">Used for model development and training.</p>
                    </div>

                    <div class="tech-card">
                        <div class="tech-card-header">
                            <span class="tech-icon">🔬</span>
                            <h3 class="tech-title">Grad-CAM</h3>
                        </div>
                        <p class="tech-desc">Provides visual interpretability for model predictions.</p>
                    </div>

                    <div class="tech-card">
                        <div class="tech-card-header">
                            <span class="tech-icon">🚀</span>
                            <h3 class="tech-title">FastAPI</h3>
                        </div>
                        <p class="tech-desc">Handles image upload and model inference through the backend API.</p>
                    </div>

                    <div class="tech-card">
                        <div class="tech-card-header">
                            <span class="tech-icon">⚡</span>
                            <h3 class="tech-title">ONNX Runtime</h3>
                        </div>
                        <p class="tech-desc">Enables lightweight model inference for deployment.</p>
                    </div>
                </div>
            </div>
        </section>

        <!-- 7. MODEL SCOPE -->
        <section class="model-scope-section">
            <div class="container">
                <div class="section-header text-center">
                    <span class="section-tag">Model Scope</span>
                    <h2 class="section-title">What FreshVision AI Can Classify.</h2>
                </div>

                <div class="scope-summary-grid">
                    <div class="scope-box">
                        <span class="scope-box-num">3 Fruits</span>
                        <p class="scope-box-val">Apple • Banana • Orange</p>
                    </div>
                    <div class="scope-box">
                        <span class="scope-box-num">6 Classes</span>
                        <p class="scope-box-val">Fresh Apple • Rotten Apple<br>Fresh Banana • Rotten Banana<br>Fresh Orange • Rotten Orange</p>
                    </div>
                    <div class="scope-box">
                        <span class="scope-box-num">AI Model</span>
                        <p class="scope-box-val">MobileNetV2 + Transfer Learning</p>
                    </div>
                </div>
            </div>
        </section>

        <!-- 8. BETTER RESULTS SECTION -->
        <section class="tips-section">
            <div class="container">
                <div class="section-header text-center">
                    <span class="section-tag">Better Results</span>
                    <h2 class="section-title">Better Image. Better Analysis.</h2>
                    <p class="section-lead">Simple guidelines for optimal visual classification:</p>
                </div>

                <div class="tips-cards-grid">
                    <div class="tip-card">
                        <span class="tip-check" aria-hidden="true">✓</span>
                        <div class="tip-content">
                            <h3 class="tip-title">Clear Subject</h3>
                            <p class="tip-desc">Keep the fruit clearly visible in the image.</p>
                        </div>
                    </div>

                    <div class="tip-card">
                        <span class="tip-check" aria-hidden="true">✓</span>
                        <div class="tip-content">
                            <h3 class="tip-title">Good Lighting</h3>
                            <p class="tip-desc">Avoid extremely dark or heavily overexposed images.</p>
                        </div>
                    </div>

                    <div class="tip-card">
                        <span class="tip-check" aria-hidden="true">✓</span>
                        <div class="tip-content">
                            <h3 class="tip-title">Minimal Blur</h3>
                            <p class="tip-desc">Use a reasonably sharp image for better visual information.</p>
                        </div>
                    </div>

                    <div class="tip-card">
                        <span class="tip-check" aria-hidden="true">✓</span>
                        <div class="tip-content">
                            <h3 class="tip-title">Simple Background</h3>
                            <p class="tip-desc">Reduce unnecessary visual distractions around the fruit.</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- 9. LIMITATIONS SECTION -->
        <section class="limits-section">
            <div class="container">
                <div class="section-header text-center">
                    <span class="section-tag">Transparency</span>
                    <h2 class="section-title">Know What the AI Can — and Cannot — Tell You.</h2>
                    <p class="section-lead">FreshVision AI performs visual image classification based on patterns learned from its training data.</p>
                </div>

                <div class="limits-grid">
                    <div class="limit-card">
                        <h3 class="limit-card-title">FreshVision AI Does Not:</h3>
                        <ul class="limit-list">
                            <li>✕ Detect microorganisms or toxins</li>
                            <li>✕ Guarantee food safety</li>
                            <li>✕ Determine exact shelf life</li>
                            <li>✕ Replace professional food-quality inspection</li>
                            <li>✕ Reliably classify unsupported fruits</li>
                        </ul>
                    </div>

                    <div class="limit-card limit-card-caution">
                        <h3 class="limit-card-title">Important</h3>
                        <p class="limit-desc-text">
                            FreshVision AI is an academic AI prototype designed for visual freshness classification.
                        </p>
                        <p class="limit-desc-text">
                            Predictions can be affected by image quality, lighting, background, camera angle, and other visual conditions.
                        </p>
                    </div>
                </div>
            </div>
        </section>

        <!-- 10. ABOUT SECTION -->
        <section class="about-section" id="about">
            <div class="container">
                <div class="section-header text-center">
                    <span class="section-tag">About</span>
                    <h2 class="section-title">About FreshVision AI</h2>
                </div>

                <div class="about-card-container">
                    <div class="about-text-content">
                        <p>
                            FreshVision AI is an academic deep-learning application designed to classify the visible freshness condition of apples, bananas, and oranges.
                        </p>
                        <p>
                            The system uses a MobileNetV2-based image classifier with transfer learning to distinguish between fresh and rotten fruit classes.
                        </p>
                        <p>
                            FreshVision AI combines image classification, confidence scoring, and Grad-CAM visualization to make AI predictions easier to understand.
                        </p>
                    </div>

                    <div class="about-project-scope-banner">
                        <div class="scope-item">
                            <span class="scope-title">Project Scope</span>
                            <span class="scope-value">3 Fruits • 6 Classes • Deep Learning</span>
                        </div>
                        <div class="scope-item">
                            <span class="scope-title">Classification Classes</span>
                            <span class="scope-value">Fresh Apple • Rotten Apple • Fresh Banana • Rotten Banana • Fresh Orange • Rotten Orange</span>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- 11. FINAL CALL TO ACTION -->
        <section class="final-cta-section">
            <div class="container">
                <div class="cta-inner-card text-center">
                    <h2 class="cta-headline">Ready to See What AI Sees?</h2>
                    <p class="cta-sub">
                        Upload an apple, banana, or orange image and get an AI-powered classification with confidence and visual explanation.
                    </p>
                    <div class="cta-actions">
                        <a href="#detect" class="btn btn-primary btn-lg">
                            <span>Try FreshVision AI</span>
                            <span class="btn-arrow" aria-hidden="true">→</span>
                        </a>
                    </div>
                </div>
            </div>
        </section>
    </main>

    <!-- FOOTER -->
    <footer class="footer">
        <div class="container footer-container">
            <div class="footer-top-grid">
                <!-- Col 1: Brand Info -->
                <div class="footer-col footer-col-brand">
                    <a href="#home" class="brand footer-brand">
                        <span class="brand-icon" aria-hidden="true">🌱</span>
                        <span class="brand-text">FreshVision <span class="brand-accent">AI</span></span>
                    </a>
                    <p class="footer-tagline"><strong>AI-Powered Fruit Freshness Classification</strong></p>
                    <p class="footer-about-text">
                        Visual classification of fresh and rotten apples, bananas, and oranges using deep learning.
                    </p>
                    <div class="footer-academic-badge">
                        <span>AI Open Ended Project • SCET</span>
                    </div>
                </div>

                <!-- Col 2: Navigation Links -->
                <div class="footer-col">
                    <h4 class="footer-heading">Explore</h4>
                    <ul class="footer-links">
                        <li><a href="#home">Home</a></li>
                        <li><a href="#detect">Detect</a></li>
                        <li><a href="#how-it-works">How It Works</a></li>
                        <li><a href="#about">About</a></li>
                    </ul>
                </div>

                <!-- Col 3: Technology -->
                <div class="footer-col">
                    <h4 class="footer-heading">Technology</h4>
                    <ul class="footer-links">
                        <li>MobileNetV2</li>
                        <li>PyTorch</li>
                        <li>Transfer Learning</li>
                        <li>Grad-CAM</li>
                        <li>FastAPI</li>
                        <li>ONNX Runtime</li>
                    </ul>
                </div>

                <!-- Col 4: Supported Fruits -->
                <div class="footer-col">
                    <h4 class="footer-heading">Supported Fruits</h4>
                    <ul class="footer-links">
                        <li>Apple</li>
                        <li>Banana</li>
                        <li>Orange</li>
                    </ul>
                </div>
            </div>

            <div class="footer-bottom">
                <p>&copy; 2026 FreshVision AI</p>
            </div>
        </div>
    </footer>

    <script id="inlined-freshvision-scripts">
{js_content}
    </script>
</body>
</html>
"""

    # Check for Group 7 in html
    assert "group 7" not in html.lower(), "Found Group 7 in generated HTML!"
    print("[+] Verified: ZERO occurrences of 'Group 7' in HTML!")

    out_path = os.path.join('templates', 'index.html')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"[+] Successfully wrote {out_path}! Size: {len(html)} bytes")

if __name__ == '__main__':
    build()

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi.testclient import TestClient
from app import app
import json

client = TestClient(app)

# 1. Homepage
r = client.get('/')
assert r.status_code == 200
print('[PASS] GET / returned 200')

# 2. Metrics
r = client.get('/api/metrics')
assert r.status_code == 200
metrics = r.json()
acc = metrics.get('overall_accuracy_pct')
samples = metrics.get('test_samples')
print(f'[PASS] GET /api/metrics returned 200 | Test Accuracy: {acc}% | Samples: {samples}')
assert acc == 98.37, f"Expected 98.37%, got {acc}%"

# 3. Presets
presets = ['fresh_apple', 'rotten_apple', 'fresh_banana', 'rotten_banana', 'fresh_orange', 'rotten_orange']
for p in presets:
    r = client.get(f'/api/sample/{p}')
    assert r.status_code == 200, f'Failed for preset {p}: {r.status_code}'
    data = r.json()
    assert 'prediction' in data and 'confidence_pct' in data and 'gradcam_b64' in data
    pred = data['prediction']
    fruit = data['fruit_type']
    conf = data['confidence_pct']
    gcam_len = len(data['gradcam_b64'])
    print(f'  [PASS] Preset {p:15s} -> Predicted: {pred:6s} | Fruit: {fruit:6s} | Conf: {conf:.2f}% | Grad-CAM b64: {gcam_len} chars')

# 4. Error Handling: Corrupt image file
r_corrupt = client.post('/api/predict', files={'file': ('corrupt.png', b'not_a_valid_png_content', 'image/png')})
assert r_corrupt.status_code == 400, f'Expected 400 for corrupt image, got {r_corrupt.status_code}'
detail = r_corrupt.json()['detail']
print(f'[PASS] Corrupt image rejected with HTTP {r_corrupt.status_code}: "{detail}"')

# 5. Error Handling: Non-image mime type
r_txt = client.post('/api/predict', files={'file': ('notes.txt', b'hello text', 'text/plain')})
assert r_txt.status_code == 400, f'Expected 400 for text file, got {r_txt.status_code}'
detail2 = r_txt.json()['detail']
print(f'[PASS] Non-image file rejected with HTTP {r_txt.status_code}: "{detail2}"')

print('\n--- ALL FASTAPI & REAL INFERENCE SMOKE TESTS PASSED ---')

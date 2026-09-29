import sys
import os
import traceback
from pathlib import Path

# Add project root directory and current working directory to sys.path
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

cwd = os.getcwd()
if cwd not in sys.path:
    sys.path.insert(0, cwd)

try:
    from app import app
except Exception as e:
    from fastapi import FastAPI
    from fastapi.responses import HTMLResponse

    app = FastAPI(title="FreshVision AI - Boot Error")
    tb = traceback.format_exc()
    cwd_files = []
    try:
        for r, d, f in os.walk(os.getcwd()):
            for file in f:
                cwd_files.append(os.path.relpath(os.path.join(r, file), os.getcwd()))
            if len(cwd_files) > 50:
                break
    except Exception:
        pass

    @app.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE"])
    def boot_error(full_path: str = ""):
        return HTMLResponse(
            f"<html><body style='font-family:sans-serif;padding:24px;background:#0d1117;color:#e6edf3;'>"
            f"<h2 style='color:#f85149;'>Startup Exception in FreshVision AI</h2>"
            f"<pre style='background:#161b22;padding:16px;border-radius:8px;border:1px solid #30363d;color:#ff7b72;overflow:auto;'>{tb}</pre>"
            f"<h4>Environment Info:</h4>"
            f"<ul>"
            f"<li><b>CWD:</b> {os.getcwd()}</li>"
            f"<li><b>sys.path:</b> {sys.path}</li>"
            f"<li><b>Files in CWD:</b> {cwd_files[:30]}</li>"
            f"</ul>"
            f"</body></html>",
            status_code=500
        )

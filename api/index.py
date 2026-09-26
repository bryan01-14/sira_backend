import os
import sys
import traceback
from fastapi import FastAPI
from fastapi.responses import JSONResponse

# 1. Add potential project directories to sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API_DIR = os.path.dirname(os.path.abspath(__file__))
CWD = os.getcwd()

for p in [BASE_DIR, API_DIR, CWD, os.path.join(CWD, "Backend")]:
    if p and p not in sys.path:
        sys.path.insert(0, p)

import_error = None
try:
    from app.main import app as main_app
    app = main_app
except Exception as e:
    import_error = traceback.format_exc()
    # Create emergency diagnostic app
    app = FastAPI(title="SIRA Backend Diagnostic")
    
    @app.get("/{full_path:path}")
    def diagnostic_fallback(full_path: str = ""):
        return JSONResponse(
            status_code=500,
            content={
                "error": "FastAPI App Import Failed on Vercel",
                "details": import_error,
                "sys_path": sys.path,
                "files_in_base": os.listdir(BASE_DIR) if os.path.exists(BASE_DIR) else [],
                "cwd": CWD
            }
        )

# Export handler
handler = app



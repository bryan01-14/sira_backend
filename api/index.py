import os
import sys

# Ensure backend root directory is in python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app

# Vercel Serverless ASGI handler
try:
    from mangum import Mangum
    handler = Mangum(app, lifespan="off")
except Exception:
    handler = app

# Export for both ASGI direct and Mangum serverless
app = app


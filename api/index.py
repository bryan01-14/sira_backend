import os
import sys

# Ensure backend root directory is in python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app

# Vercel Serverless WSGI/ASGI handler entrypoint
handler = app

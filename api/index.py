import os
import sys
import urllib.parse

# Ensure backend root directory is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app as fastapi_app

async def app(scope, receive, send):
    if scope["type"] == "http":
        qs = scope.get("query_string", b"").decode("latin1")
        if "__path__=" in qs:
            params = urllib.parse.parse_qs(qs, keep_blank_values=True)
            path_list = params.pop("__path__", [])
            if path_list:
                target_path = path_list[0]
                clean_path = "/" + target_path.lstrip("/") if target_path else "/"
                scope["path"] = clean_path
                scope["raw_path"] = clean_path.encode("latin1")
                scope["root_path"] = ""
                new_qs = urllib.parse.urlencode(params, doseq=True)
                scope["query_string"] = new_qs.encode("latin1")
    await fastapi_app(scope, receive, send)




import os
import sys
import json

# Ensure backend root directory is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app as fastapi_app

async def app(scope, receive, send):
    if scope.get("type") == "http":
        headers = {k.decode("latin1"): v.decode("latin1") for k, v in scope.get("headers", [])}
        data = {
            "scope_path": scope.get("path"),
            "scope_raw_path": str(scope.get("raw_path")),
            "scope_root_path": scope.get("root_path"),
            "scope_query_string": scope.get("query_string", b"").decode("latin1"),
            "scope_server": scope.get("server"),
            "headers": headers
        }
        body = json.dumps(data, indent=2).encode("utf-8")
        await send({
            "type": "http.response.start",
            "status": 200,
            "headers": [
                [b"content-type", b"application/json"],
                [b"content-length", str(len(body)).encode("utf-8")]
            ]
        })
        await send({
            "type": "http.response.body",
            "body": body
        })
        return
    await fastapi_app(scope, receive, send)


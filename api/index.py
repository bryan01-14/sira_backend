import os
import sys
import json
import urllib.parse

# Ensure backend root directory is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app as fastapi_app

async def app(scope, receive, send):
    if scope["type"] == "http":
        qs = scope.get("query_string", b"").decode("utf-8")
        if "debug-scope" in scope.get("path", "") or "debug-scope" in qs:
            body = json.dumps({
                "path": scope.get("path"),
                "root_path": scope.get("root_path"),
                "raw_path": str(scope.get("raw_path")),
                "query_string": qs,
                "headers": [[k.decode("latin1"), v.decode("latin1")] for k, v in scope.get("headers", [])]
            }, indent=2).encode("utf-8")
            await send({
                "type": "http.response.start",
                "status": 200,
                "headers": [[b"content-type", b"application/json"]]
            })
            await send({
                "type": "http.response.body",
                "body": body
            })
            return

        scope["root_path"] = ""
        if "__route__=" in qs:
            params = urllib.parse.parse_qs(qs, keep_blank_values=True)
            route_list = params.pop("__route__", [])
            if route_list:
                route = route_list[0]
                clean_route = "/" + route.lstrip("/") if route else "/"
                scope["path"] = clean_route
                scope["raw_path"] = clean_route.encode("utf-8")
                new_qs = urllib.parse.urlencode(params, doseq=True)
                scope["query_string"] = new_qs.encode("utf-8")
        else:
            path = scope.get("path", "")
            for prefix in ["/api/index.py", "/api/index"]:
                if path.startswith(prefix):
                    path = path[len(prefix):]
                    break
            clean_route = "/" + path.lstrip("/") if path else "/"
            scope["path"] = clean_route
            scope["raw_path"] = clean_route.encode("utf-8")

    await fastapi_app(scope, receive, send)







from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine, Base
import app.models  # Assure que tous les modèles SQLAlchemy sont chargés


from app.routers import (
    auth_router,
    users_router,
    transport_router,
    fares_router,
    incidents_router,
    routing_router,
    voice_router,
)

app = FastAPI(
    title="SIRA Backend API",
    description="""
    ## 🚍 SIRA - Plateforme de Mobilité Intelligente à Abidjan
    
    API REST complète dédiée à l'intégration des transports formels (**SOTRA**) et informels (**Gbaka, Wôrô-wôrô**), avec :
    - 🔐 **Authentification OTP & JWT** (intégration Orange Côte d'Ivoire / Supabase)
    - 🗺️ **Moteur d'itinéraires multimodaux** & calcul de temps / coûts optimisés
    - 💰 **Tarification communautaire** avec score de confiance et validation croisée
    - ⚠️ **Signalements en temps réel** (bouchons, inondations, accidents) et alertes
    - 🎙️ **Assistant vocal & NLP** adapté au contexte ivoirien
    """,
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request

class VercelPathMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.scope.get("path", "")
        
        # Check headers passed by Vercel for the original path
        for h in ["x-matched-path", "x-invoke-path", "x-forwarded-uri"]:
            header_val = request.headers.get(h)
            if header_val and not header_val.startswith("/api/index"):
                path = header_val.split("?")[0]
                break
        
        # Clean serverless function prefixes if present
        for prefix in ["/api/index.py", "/api/index"]:
            if path.startswith(prefix):
                path = path[len(prefix):]
                break
                
        if not path or path == "":
            path = "/"
            
        request.scope["path"] = path
        return await call_next(request)

app.add_middleware(VercelPathMiddleware)


# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Route racine & de santé
@app.get("/", tags=["Système"], summary="Accueil API SIRA")
def root():
    return {
        "status": "OK",
        "app": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "docs": "/docs"
    }

@app.get("/debug-headers", tags=["Système"])
def debug_headers(request: Request):
    return {
        "headers": dict(request.headers),
        "scope_path": request.scope.get("path"),
        "raw_path": str(request.scope.get("raw_path", b"")),
        "url_path": request.url.path
    }

@app.get("/health", tags=["Système"], summary="Statut du serveur SIRA")

def health_check():
    return {
        "status": "OK",
        "app": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": "active"
    }


# Inclusion des routeurs API v1
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(users_router, prefix=settings.API_V1_STR)
app.include_router(transport_router, prefix=settings.API_V1_STR)
app.include_router(fares_router, prefix=settings.API_V1_STR)
app.include_router(incidents_router, prefix=settings.API_V1_STR)
app.include_router(routing_router, prefix=settings.API_V1_STR)
app.include_router(voice_router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

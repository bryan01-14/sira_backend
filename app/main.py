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

import urllib.parse
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request

class VercelPathMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        target_path = request.query_params.get("__path__")
        if target_path:
            clean_path = "/" + target_path.lstrip("/") if target_path else "/"
            request.scope["path"] = clean_path
            
            # Clean __path__ parameter from query_string
            qs = request.scope.get("query_string", b"").decode("latin1")
            params = urllib.parse.parse_qs(qs, keep_blank_values=True)
            params.pop("__path__", None)
            new_qs = urllib.parse.urlencode(params, doseq=True)
            request.scope["query_string"] = new_qs.encode("latin1")
        elif request.scope.get("path", "").startswith("/api/index.py"):
            rest = request.scope.get("path", "")[len("/api/index.py"):]
            request.scope["path"] = rest if rest else "/"
        elif request.scope.get("path", "").startswith("/api/index"):
            rest = request.scope.get("path", "")[len("/api/index"):]
            request.scope["path"] = rest if rest else "/"

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

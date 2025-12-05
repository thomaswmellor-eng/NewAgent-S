"""
API Backend pour Agent S3 - Interface SaaS
FastAPI server qui expose Agent S3 via WebSocket pour streaming en temps réel
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
import json
import os
from dotenv import load_dotenv
from typing import Optional
import logging

# Importer Agent S3
try:
    # Import relatif si exécuté comme module (Azure)
    from .agent_runner import AgentS3Runner
except ImportError:
    # Import absolu si exécuté directement (développement local)
    from agent_runner import AgentS3Runner

# Configuration
load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(title="Agent S3 API", version="1.0.0")

# CORS pour l'extension
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En production, spécifiez les domaines autorisés
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instance globale de l'agent (optimisation)
agent_runner: Optional[AgentS3Runner] = None

# Flag pour arrêter l'exécution en cours
stop_execution = False


class TaskRequest(BaseModel):
    """Requête pour exécuter une tâche"""
    prompt: str
    enable_reflection: bool = True


class TaskResponse(BaseModel):
    """Réponse après exécution"""
    success: bool
    message: str
    action: Optional[str] = None
    error: Optional[str] = None


@app.on_event("startup")
async def startup_event():
    """Initialiser Agent S3 au démarrage"""
    global agent_runner
    try:
        logger.info("🚀 Initialisation d'Agent S3...")
        agent_runner = AgentS3Runner()
        logger.info("✅ Agent S3 initialisé avec succès")
    except Exception as e:
        logger.error(f"❌ Erreur lors de l'initialisation: {e}")
        raise


@app.get("/")
async def root():
    """Health check"""
    return {
        "status": "online",
        "service": "Agent S3 API",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Vérifier l'état de l'API et de l'agent"""
    if agent_runner is None:
        raise HTTPException(status_code=503, detail="Agent not initialized")

    return {
        "status": "healthy",
        "agent_initialized": agent_runner is not None,
        "config": {
            "claude_model": os.getenv("AZURE_OPENAI_NAME"),
            "fara_model": os.getenv("AZURE_FARA_NAME"),
        }
    }


@app.websocket("/ws/agent")
async def websocket_agent(websocket: WebSocket):
    """
    WebSocket pour communication en temps réel avec Agent S3
    Permet le streaming des réflexions et actions
    """
    global stop_execution
    await websocket.accept()
    logger.info("🔌 Client WebSocket connecté")

    try:
        while True:
            # Recevoir le prompt du client
            data = await websocket.receive_text()
            request_data = json.loads(data)

            # Check if it's a stop command
            if request_data.get("command") == "stop":
                stop_execution = True
                logger.info("⛔ Commande d'arrêt reçue")
                await websocket.send_json({
                    "type": "stopped",
                    "message": "⛔ Exécution arrêtée par l'utilisateur"
                })
                continue

            prompt = request_data.get("prompt")

            if not prompt:
                await websocket.send_json({
                    "type": "error",
                    "message": "Prompt vide"
                })
                continue

            logger.info(f"📝 Prompt reçu: {prompt}")

            # Reset stop flag for new execution
            stop_execution = False

            # Envoyer confirmation
            await websocket.send_json({
                "type": "status",
                "message": "Traitement en cours..."
            })

            try:
                # Exécuter la tâche avec streaming
                async for event in agent_runner.execute_task_stream(prompt, lambda: stop_execution):
                    # Check if user requested stop
                    if stop_execution:
                        await websocket.send_json({
                            "type": "stopped",
                            "message": "⛔ Exécution arrêtée par l'utilisateur"
                        })
                        break

                    # Envoyer chaque événement au client
                    await websocket.send_json(event)

            except Exception as e:
                logger.error(f"❌ Erreur lors de l'exécution: {e}")
                await websocket.send_json({
                    "type": "error",
                    "message": f"Erreur: {str(e)}"
                })

    except WebSocketDisconnect:
        logger.info("🔌 Client WebSocket déconnecté")
    except Exception as e:
        logger.error(f"❌ Erreur WebSocket: {e}")
        await websocket.close()


@app.post("/api/task", response_model=TaskResponse)
async def execute_task(request: TaskRequest):
    """
    Endpoint REST pour exécuter une tâche (alternative au WebSocket)
    Utilisé pour des requêtes simples sans streaming
    """
    if agent_runner is None:
        raise HTTPException(
            status_code=503,
            detail="Agent non initialisé"
        )

    try:
        logger.info(f"📝 Exécution de la tâche: {request.prompt}")

        result = await agent_runner.execute_task(
            prompt=request.prompt,
            enable_reflection=request.enable_reflection
        )

        return TaskResponse(
            success=True,
            message="Tâche exécutée avec succès",
            action=result.get("action"),
        )

    except Exception as e:
        logger.error(f"❌ Erreur: {e}")
        return TaskResponse(
            success=False,
            message="Erreur lors de l'exécution",
            error=str(e)
        )


@app.get("/api/config")
async def get_config():
    """Obtenir la configuration actuelle"""
    return {
        "models": {
            "main": os.getenv("AZURE_OPENAI_NAME"),
            "grounding": os.getenv("AZURE_FARA_NAME"),
        },
        "resolution": {
            "width": os.getenv("GROUNDING_WIDTH", "1920"),
            "height": os.getenv("GROUNDING_HEIGHT", "1080"),
        }
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )

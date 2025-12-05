"""
Agent S3 Runner - Wrapper pour exécuter Agent S3 de manière asynchrone
Gère l'initialisation et l'exécution des tâches avec streaming
"""

import os
import asyncio
import io
from typing import AsyncGenerator, Dict, Any
from dotenv import load_dotenv
import logging

# Import pyautogui seulement si disponible (pas sur Azure)
try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
except (ImportError, KeyError):
    PYAUTOGUI_AVAILABLE = False
    print("⚠️ PyAutoGUI not available - screenshot capture disabled")

from gui_agents.s3.agents.agent_s import AgentS3
from gui_agents.s3.agents.grounding import OSWorldACI

load_dotenv()
logger = logging.getLogger(__name__)


class AgentS3Runner:
    """Wrapper pour exécuter Agent S3 de manière asynchrone"""

    def __init__(self):
        """Initialiser Agent S3 avec la configuration depuis .env"""

        logger.info("🔧 Chargement de la configuration...")

        # Configuration Claude Sonnet 4.5
        self.engine_params = {
            "engine_type": "azure",
            "model": os.getenv("AZURE_OPENAI_NAME"),
            "base_url": os.getenv("AZURE_OPENAI_ENDPOINT"),
            "api_key": os.getenv("AZURE_OPENAI_API_KEY"),
            "api_version": os.getenv("OPENAI_API_VERSION", "2024-08-01-preview"),
        }

        # Configuration Fara-7B
        fara_endpoint = os.getenv("AZURE_FARA_ENDPOINT")
        if not fara_endpoint.endswith("/v1"):
            fara_endpoint = fara_endpoint.rstrip("/") + "/v1"

        self.engine_params_for_grounding = {
            "engine_type": "vllm",
            "model": os.getenv("AZURE_FARA_NAME"),
            "base_url": fara_endpoint,
            "api_key": os.getenv("AZURE_FARA_API_KEY"),
            "grounding_width": int(os.getenv("GROUNDING_WIDTH", "1920")),
            "grounding_height": int(os.getenv("GROUNDING_HEIGHT", "1080")),
        }

        # Initialiser le grounding agent
        logger.info("🎯 Initialisation du grounding agent...")
        # env=None means no local coding environment (safer for web API)
        self.grounding_agent = OSWorldACI(
            env=None,  # Required argument - None disables code execution environment
            platform="windows",
            engine_params_for_generation=self.engine_params,
            engine_params_for_grounding=self.engine_params_for_grounding,
            width=1920,
            height=1080
        )

        # Initialiser Agent S3
        logger.info("🧠 Initialisation d'Agent S3...")
        self.agent = AgentS3(
            self.engine_params,
            self.grounding_agent,
            platform="windows",
            max_trajectory_length=8,
            enable_reflection=True
        )

        logger.info("✅ Agent S3 initialisé avec succès!")

    def capture_screenshot(self) -> bytes:
        """Capturer l'écran et retourner les bytes"""
        if not PYAUTOGUI_AVAILABLE:
            # Sur Azure, retourner une image vide (1x1 pixel noir)
            from PIL import Image
            img = Image.new('RGB', (1, 1), color='black')
            buffered = io.BytesIO()
            img.save(buffered, format="PNG")
            return buffered.getvalue()

        screenshot = pyautogui.screenshot()
        buffered = io.BytesIO()
        screenshot.save(buffered, format="PNG")
        return buffered.getvalue()

    async def execute_task_stream(
        self,
        prompt: str,
        should_stop = lambda: False
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Exécuter une tâche avec streaming des événements
        Yield des événements: thinking, action, success, error

        Args:
            prompt: Task instruction
            should_stop: Callable that returns True if execution should stop
        """
        try:
            # Réinitialiser l'agent pour chaque nouvelle tâche
            await asyncio.to_thread(self.agent.reset)

            # Envoyer l'événement de début
            yield {
                "type": "start",
                "prompt": prompt
            }

            # Capturer l'écran
            if should_stop():
                yield {
                    "type": "stopped",
                    "message": "⛔ Exécution arrêtée par l'utilisateur"
                }
                return

            yield {
                "type": "thinking",
                "message": "📸 Capture d'écran..."
            }

            screenshot_bytes = await asyncio.to_thread(self.capture_screenshot)

            obs = {
                "screenshot": screenshot_bytes,
            }

            # Obtenir la prédiction de l'agent
            if should_stop():
                yield {
                    "type": "stopped",
                    "message": "⛔ Exécution arrêtée par l'utilisateur"
                }
                return

            yield {
                "type": "thinking",
                "message": "🧠 Traduction du prompt avec Task Planner..."
            }

            # Setup log capture to get translated instruction
            import logging
            translated_instruction = None

            class TranslationCapture(logging.Handler):
                def emit(self, record):
                    nonlocal translated_instruction
                    if "✨ Translated instruction:" in record.getMessage():
                        translated_instruction = record.getMessage().replace("✨ Translated instruction: ", "")

            capture_handler = TranslationCapture()
            agent_logger = logging.getLogger("desktopenv.agent")
            agent_logger.addHandler(capture_handler)

            # Execute task in an unlimited loop until done or user stops
            step = 0
            while True:
                # Check if user requested stop
                if should_stop():
                    yield {
                        "type": "stopped",
                        "message": "⛔ Exécution arrêtée par l'utilisateur"
                    }
                    break

                step += 1

                # Check stop before starting analysis
                if should_stop():
                    yield {
                        "type": "stopped",
                        "message": "⛔ Exécution arrêtée par l'utilisateur"
                    }
                    break

                yield {
                    "type": "thinking",
                    "message": f"🔄 Étape {step}: Analyse et planification..."
                }

                # Check stop before expensive API call
                if should_stop():
                    yield {
                        "type": "stopped",
                        "message": "⛔ Exécution arrêtée par l'utilisateur"
                    }
                    break

                # Get next action from agent
                info, action = await asyncio.to_thread(
                    self.agent.predict,
                    instruction=prompt,
                    observation=obs
                )

                # Send translated instruction on first step only
                if step == 0 and translated_instruction:
                    logger.info(f"✨ Instruction traduite: {translated_instruction}")
                    yield {
                        "type": "translated",
                        "original": prompt,
                        "translated": translated_instruction
                    }

                # Remove capture handler after first step
                if step == 0:
                    agent_logger.removeHandler(capture_handler)

                # Check stop after API call completes
                if should_stop():
                    yield {
                        "type": "stopped",
                        "message": "⛔ Exécution arrêtée par l'utilisateur"
                    }
                    break

                # Check if task is done or failed
                if "done" in action[0].lower() or "fail" in action[0].lower():
                    yield {
                        "type": "success",
                        "message": f"✅ Tâche terminée en {step} étapes!"
                    }
                    break

                # Skip this turn if action is "next" or "wait"
                if "next" in action[0].lower():
                    continue

                if "wait" in action[0].lower():
                    yield {
                        "type": "thinking",
                        "message": "⏳ Attente de 2 secondes..."
                    }
                    # Check stop before waiting
                    if should_stop():
                        yield {
                            "type": "stopped",
                            "message": "⛔ Exécution arrêtée par l'utilisateur"
                        }
                        break
                    await asyncio.sleep(2)
                    continue

                # Check stop before executing action
                if should_stop():
                    yield {
                        "type": "stopped",
                        "message": "⛔ Exécution arrêtée par l'utilisateur"
                    }
                    break

                # Send reflection if available
                if info and step == 0:  # Only send reflection on first step to avoid spam
                    yield {
                        "type": "reflection",
                        "content": str(info)[:300]  # Limit size
                    }

                # Send action plan
                yield {
                    "type": "action",
                    "content": f"Étape {step}: {action[0][:200]}...",  # Truncate for display
                    "full_action": action[0]
                }

                # Execute action
                yield {
                    "type": "thinking",
                    "message": f"⚡ Exécution de l'étape {step}..."
                }

                # Check stop right before execution
                if should_stop():
                    yield {
                        "type": "stopped",
                        "message": "⛔ Exécution arrêtée par l'utilisateur"
                    }
                    break

                try:
                    await asyncio.to_thread(exec, action[0])

                    # Check if stop was requested during execution
                    if should_stop():
                        yield {
                            "type": "stopped",
                            "message": "⛔ Exécution arrêtée par l'utilisateur"
                        }
                        break

                    await asyncio.sleep(0.5)  # Wait 0.5 second between actions

                    # Check stop before screenshot
                    if should_stop():
                        yield {
                            "type": "stopped",
                            "message": "⛔ Exécution arrêtée par l'utilisateur"
                        }
                        break

                    # Capture new screenshot for next iteration
                    screenshot_bytes = await asyncio.to_thread(self.capture_screenshot)
                    obs = {"screenshot": screenshot_bytes}

                except Exception as exec_error:
                    yield {
                        "type": "error",
                        "message": f"❌ Erreur à l'étape {step}: {str(exec_error)}"
                    }
                    break

        except Exception as e:
            logger.error(f"❌ Erreur dans execute_task_stream: {e}")
            yield {
                "type": "error",
                "message": f"❌ Erreur: {str(e)}"
            }

    async def execute_task(
        self,
        prompt: str,
        enable_reflection: bool = True
    ) -> Dict[str, Any]:
        """
        Exécuter une tâche de manière simple (sans streaming)
        Retourne le résultat final
        """
        try:
            # Capturer l'écran
            screenshot_bytes = await asyncio.to_thread(self.capture_screenshot)

            obs = {
                "screenshot": screenshot_bytes,
            }

            # Obtenir la prédiction
            info, action = await asyncio.to_thread(
                self.agent.predict,
                instruction=prompt,
                observation=obs
            )

            # Exécuter l'action
            await asyncio.to_thread(exec, action[0])

            return {
                "success": True,
                "info": info,
                "action": action[0]
            }

        except Exception as e:
            logger.error(f"❌ Erreur: {e}")
            return {
                "success": False,
                "error": str(e)
            }

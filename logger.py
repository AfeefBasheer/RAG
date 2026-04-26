import logging
import json

logging.basicConfig(level=logging.INFO, format="%(message)s", filename="app.log")
# silence noisy libraries
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("postgrest").setLevel(logging.WARNING)
logging.getLogger("supabase").setLevel(logging.WARNING)
logging.getLogger("app").setLevel(logging.INFO)


logger = logging.getLogger("app")


def log_event(event: str, **kwargs):
    logger.info(json.dumps({"event": event, **kwargs}, ensure_ascii=False))

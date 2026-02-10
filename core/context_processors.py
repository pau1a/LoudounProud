from pathlib import Path
from typing import Any, Dict

from django.conf import settings


def base_context(request) -> Dict[str, Any]:
    return {
        "debug": settings.DEBUG,
        "allowed_hosts": settings.ALLOWED_HOSTS,
        "base_dir": str(Path(settings.BASE_DIR).name),
    }

"""Android foreground-service entry point for the upstream CUKTECH server."""
from __future__ import annotations

import asyncio
import os
import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
UPSTREAM = ROOT / "upstream"


def _runtime_dir() -> Path:
    """Use Android's private writable storage, never the packaged APK assets."""
    try:
        from android.storage import app_storage_path
        location = Path(app_storage_path()) / "cuktech"
    except ImportError:
        location = ROOT / "data"
    location.mkdir(parents=True, exist_ok=True)
    return location


def main() -> None:
    if not (UPSTREAM / "ha_server.py").exists():
        raise RuntimeError(
            "The upstream server has not been prepared. Run tools/prepare_upstream.py before building the APK."
        )
    runtime = _runtime_dir()
    config = runtime / "config.yaml"
    if not config.exists():
        shutil.copy2(UPSTREAM / "data" / "config.yaml", config)
    os.environ.setdefault("CUKTECH_CONFIG_PATH", str(config))
    os.environ.setdefault("CUKTECH_HISTORY_DB_PATH", str(runtime / "port_history.db"))
    os.environ.setdefault("CUKTECH_ANDROID", "1")
    sys.path.insert(0, str(UPSTREAM))
    from ha_server import app, get_server  # Imported only after source preparation.
    from aiohttp import web

    server = get_server()
    web.run_app(app, host="0.0.0.0", port=server.config.server.port, handle_signals=False)


if __name__ == "__main__":
    main()

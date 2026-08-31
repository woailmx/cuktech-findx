"""Copy upstream code and apply the minimal Android-only BLE recovery patch.

Usage: python tools/prepare_upstream.py /path/to/cuktech-ble-server
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path


REQUIRED = (
    "ha_server.py", "ble_manager.py", "config.py", "state.py", "history.py",
    "energy.py", "xiaomi_cloud.py", "bemfa_client.py", "downsample.py",
    "config.yaml.example",
)


def patch_ble_manager(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    marker = "def _has_bluetoothctl():\n"
    replacement = (
        "def _has_bluetoothctl():\n"
        "    \"\"\"Android uses Bleak's native backend; no BlueZ helper is available.\"\"\"\n"
        "    if os.environ.get(\"CUKTECH_ANDROID\") == \"1\":\n"
        "        return False\n"
    )
    if marker not in text:
        raise RuntimeError("Unsupported upstream ble_manager.py: bluetoothctl helper not found")
    text = text.replace(marker, replacement, 1)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python tools/prepare_upstream.py /path/to/cuktech-ble-server")
    source = Path(sys.argv[1]).resolve()
    if not (source / "ha_server.py").is_file():
        raise SystemExit(f"Not an upstream checkout: {source}")
    destination = Path(__file__).resolve().parents[1] / "app" / "upstream"
    if destination.exists():
        shutil.rmtree(destination)
    destination.mkdir(parents=True)
    for item in REQUIRED:
        shutil.copy2(source / item, destination / item)
    shutil.copytree(source / "src", destination / "src")
    shutil.copytree(source / "web", destination / "web")
    (destination / "data").mkdir()
    shutil.copy2(source / "config.yaml.example", destination / "data" / "config.yaml")
    patch_ble_manager(destination / "ble_manager.py")
    print(f"Prepared Android service source at {destination}")


if __name__ == "__main__":
    main()

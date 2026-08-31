"""Android-only permission, battery and foreground-service helpers."""
from __future__ import annotations


class AndroidBridge:
    def request_bluetooth_permissions(self) -> bool:
        try:
            from android.permissions import Permission, check_permission, request_permissions
            needed = [Permission.BLUETOOTH_SCAN, Permission.BLUETOOTH_CONNECT]
            if all(check_permission(permission) for permission in needed):
                return True
            request_permissions(needed)
            return False
        except ImportError:
            # Keeps desktop UI development usable; Android is enforced by the manifest.
            return True

    def start_service(self) -> None:
        from android import AndroidService
        AndroidService("CUKTECH BLE 正在运行", "保持蓝牙连接与局域网控制台").start("start")

    def open_battery_settings(self) -> None:
        try:
            from jnius import autoclass
            PythonActivity = autoclass("org.kivy.android.PythonActivity")
            Intent = autoclass("android.content.Intent")
            Settings = autoclass("android.provider.Settings")
            activity = PythonActivity.mActivity
            activity.startActivity(Intent(Settings.ACTION_IGNORE_BATTERY_OPTIMIZATION_SETTINGS))
        except Exception:
            # The user can still reach this screen manually on vendor ROMs.
            pass

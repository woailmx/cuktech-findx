"""Small Android control screen for the CUKTECH background service."""
from __future__ import annotations

import socket

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

from android_bridge import AndroidBridge


class CuktechApp(App):
    def build(self):
        self.bridge = AndroidBridge()
        root = BoxLayout(orientation="vertical", padding=24, spacing=16)
        self.status = Label(text="正在检查蓝牙权限…", halign="left", valign="top")
        self.status.bind(size=lambda w, _: setattr(w, "text_size", w.size))
        root.add_widget(self.status)

        start = Button(text="启动充电器服务", size_hint_y=None, height=52)
        start.bind(on_release=lambda _: self.start_service())
        root.add_widget(start)

        battery = Button(text="打开电池优化设置", size_hint_y=None, height=52)
        battery.bind(on_release=lambda _: self.bridge.open_battery_settings())
        root.add_widget(battery)
        Clock.schedule_once(lambda _: self.refresh(), 0)
        return root

    def refresh(self):
        address = self._dashboard_address()
        if not self.bridge.request_bluetooth_permissions():
            self.status.text = "请允许附近设备/蓝牙权限，然后再点“启动充电器服务”。"
            return
        self.status.text = (
            "蓝牙权限已准备。\n\n"
            "启动后，控制台地址为：\n"
            f"{address}\n\n"
            "若锁屏后服务停止，请点下方按钮并将应用设为不受电池优化限制。"
        )

    def start_service(self):
        if not self.bridge.request_bluetooth_permissions():
            self.refresh()
            return
        self.bridge.start_service()
        self.status.text = "服务已请求启动。请保留通知栏中的“CUKTECH BLE 正在运行”通知。\n\n" + self._dashboard_address()

    @staticmethod
    def _dashboard_address() -> str:
        try:
            ip = socket.gethostbyname(socket.gethostname())
        except OSError:
            ip = "手机局域网 IP"
        return f"http://{ip}:8199/"


if __name__ == "__main__":
    CuktechApp().run()

[app]
title = CUKTECH BLE
package.name = cuktechble
package.domain = io.github.kairui1108
source.dir = app
source.include_exts = py,png,jpg,kv,html,css,js,yaml,json
version = 0.1.0
requirements = python3,kivy,aiohttp,paho-mqtt,cryptography,pyyaml,requests,pycryptodomex,sqlite3,bleak
orientation = portrait
fullscreen = 0
services = CuktechBLE:service/main.py:foreground
android.permissions = BLUETOOTH,BLUETOOTH_ADMIN,BLUETOOTH_SCAN,BLUETOOTH_CONNECT,ACCESS_FINE_LOCATION,FOREGROUND_SERVICE,FOREGROUND_SERVICE_CONNECTED_DEVICE,WAKE_LOCK,INTERNET,ACCESS_NETWORK_STATE
android.api = 33
android.minapi = 26
android.archs = arm64-v8a
android.allow_backup = False
android.accept_sdk_license = True
p4a.local_recipes = vendor/bleak/bleak/backends/p4android/recipes

[buildozer]
log_level = 2
warn_on_root = 1

# CUKTECH BLE for Android — Find X prototype

This project packages the upstream CUKTECH BLE server as an Android application.
It is intended for an OPPO Find X (Android 11), without root access and without
Home Assistant. The first release keeps the upstream web dashboard and BLE
protocol but starts them from an Android foreground service instead of systemd.

## Current scope

* Android Bluetooth runtime permissions.
* A foreground service, so ColorOS is less likely to terminate the server.
* A small on-phone control screen with the dashboard address and battery
  optimisation guidance.
* A well-defined source import location for the upstream project.

The phone-facing service is deliberately unable to start until the upstream
source tree has been imported into `upstream/`. This prevents an APK from
silently presenting a dashboard without its real charger protocol.

## Required upstream source

Copy a checkout of `kairui1108/cuktech-ble-server` into `upstream/`, preserving
these paths:

* `ha_server.py`, `ble_manager.py`, `config.py`, `state.py`, `history.py`,
  `energy.py`, `xiaomi_cloud.py`, and `bemfa_client.py`
* `src/cuktech_ble/`
* `web/`
* `config.yaml.example`

Run `tools/prepare_upstream.py` before building. It copies the required source
into the Android service package and changes only Linux-specific `bluetoothctl`
recovery calls into no-ops on Android. Normal BLE scanning, GATT connection,
authentication, and notifications are left to Bleak's Android backend.

Bleak's Android backend includes both Python and small Java callback classes.
Before building, clone its source in `vendor/bleak/`; `buildozer.spec` registers
Bleak's own Python-for-Android recipe from that exact directory. Installing
`bleak` with pip alone is not enough because it omits the Android build recipe.

## Build host

Buildozer/Python-for-Android needs an Ubuntu or Debian build host. Do not run
this part on the phone. Build output is an APK, which is then installed on the
Find X. The Android 11 phone itself does not need root.

On the build host, run the following from this project directory after the
upstream checkout is available:

```bash
git clone --depth 1 https://github.com/hbldh/bleak.git vendor/bleak
python3 tools/prepare_upstream.py /path/to/cuktech-ble-server
buildozer android debug
```

The first build downloads the Android SDK/NDK and can take a long time. The
result will be under `bin/`.

## Cloud build alternative

The included GitHub Actions workflow at `.github/workflows/build-apk.yml` builds
the same debug APK on an Ubuntu runner. Push this project to a private GitHub
repository, then open the repository's **Actions** tab and run **Build Find X
Android APK**. When it finishes, download the `cuktech-ble-findx-debug`
artifact; it contains the APK or the build logs if a dependency needs adjustment.

Use a private repository. Do not commit a real device token, BLE key, Wi-Fi
password, or copied `app/upstream/data/config.yaml`.

## First-device test checklist

1. Install the signed debug APK and accept **Nearby devices** / Bluetooth
   permissions.
2. Start the service from the app and keep its persistent notification visible.
3. In ColorOS battery settings, select the app and allow background operation;
   also disable battery optimisation for it.
4. Put the phone and charger within one metre, then open the printed dashboard
   address from another device on the same Wi-Fi.
5. Test a 30-minute locked-screen run, then an overnight run. Only after both
   are stable should MQTT or Home Assistant be enabled.

## Security note

The dashboard contains access to the charger and configuration secrets. Keep it
on a trusted home LAN. This prototype does not expose the phone to the public
Internet and should not be port-forwarded.

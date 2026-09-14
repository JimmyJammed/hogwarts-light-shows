# Configuration and API

Version 1 show JSON requires name, positive finite duration, roles (logical name → device ID), and a nonempty cues list. Each cue contains at (seconds within duration), role, action, and value. Supported actions: brightness (integer 0..100), color (three integer RGB channels 0..255), power (boolean), scene (name from a Govee Profile). Optional audio resolves relative to the show file and must exist.

Commands: validate checks show syntax/assets; preview prints timestamp order; simulate runs virtual devices; run requires a hardware profile. Device availability and scene mappings are checked before playback. A profile uses the Govee version 1 format.

Python: `load(path)` returns validated configuration; `await play(config, client, profile, simulate=True)` returns RunResult. Supply a loaded configuration. Cancellation waits for restoration. The app does not implement its own scheduler or device protocol.

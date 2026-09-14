# Validation — 2026-09-14

On macOS arm64: seven pytest tests passed on Python 3.12.13, 3.13.15, and 3.14.6. They cover malformed timestamps/roles/values, missing audio/devices, repeated playback, cancellation, and restoration.

Wheel and source archive built. A fresh environment installed the wheel and fetched its two pinned dependencies directly from public GitHub without sibling checkouts. Installed validate, preview, and simulate commands ran outside the repository. The bundled original tones were included in the wheel.

No physical Govee hardware, Raspberry Pi, Windows, or actual audio-output verification was performed. Simulation output is a demonstration, not device verification. Package registry publication was not performed.

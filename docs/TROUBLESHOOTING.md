# Troubleshooting

Missing role/device: regenerate the profile and update the role's device ID. Missing scene: add it to the Govee profile. Missing audio: paths are relative to the show JSON; copy the referenced file. No audio backend: install aplay on Linux or omit audio for silent runs.

Restoration failure: the device may have disconnected; inspect the exception group for each attempted device. Network timeouts are bounded by the Govee transport, but real hardware recovery cannot be guaranteed. Do not claim successful restoration when a command was merely sent.

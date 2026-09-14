# Setup and hardware

Start with README simulation. On macOS use Python 3.12+ and the built-in afplay backend. On Raspberry Pi/Linux use Python 3.12+ and install ALSA's aplay for audio. Without those executables, omit the audio field. Windows simulation works in principle; live audio currently requires a custom application adapter.

Enable Govee LAN control. Run `govee --live discover --output devices.json`. Map the role values in your show JSON to the discovered device IDs. Then use `wizard-show run --show show.json --profile devices.json`. The run command is explicitly live and requires a profile. Status snapshots must succeed before any cue starts; cleanup restores reported device state.

Do not use simulated device addresses for live shows. Keep a single process in charge of the LAN response port. Audio and network timing are best-effort.

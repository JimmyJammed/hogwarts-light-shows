# Hogwarts Light Shows

An original wizard-themed show starter using Light Show Manager and Govee LAN API Plus. Python 3.12+ · MIT · 0.1.0.

## First run

```sh
git clone https://github.com/JimmyJammed/hogwarts-light-shows.git
cd hogwarts-light-shows
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e '.[dev]'
wizard-show validate
wizard-show preview
wizard-show simulate
```

Git is required to install the two dependencies pinned to merged GitHub revisions. No sibling checkout, account, device, or private registry is needed. The bundled Lantern Spell uses simulated lights and original generated tones. Simulation prints audio cues without playing sound.

```text
 0.00s | lantern | color [255, 170, 70]
 0.40s | lantern | brightness 80
 1.00s | lantern | color [70, 100, 255]
 1.60s | lantern | brightness 20
```

## Make it yours

Copy the bundled lanterns.json and spell.wav from src/hogwarts_light_shows/assets. Edit timestamps, colors, brightness, device roles, and optional audio. Run `wizard-show simulate --show path/to/show.json`. Your own audio remains yours; no film soundtrack is included.

[Setup](docs/GETTING_STARTED.md) · [Configuration/API](docs/API.md) · [Customization](docs/CUSTOMIZATION.md) · [Architecture](docs/ARCHITECTURE.md) · [Migration](docs/MIGRATION.md) · [Testing](docs/TESTING.md) · [Validation](docs/VALIDATION.md) · [Troubleshooting](docs/TROUBLESHOOTING.md)

## License

[MIT](LICENSE). This is an unofficial community project. The sample cue sequence and tones are original; no franchise audio or artwork is bundled.

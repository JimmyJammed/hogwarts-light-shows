# Testing

Install the development extra and run pytest. Tests cover malformed cues, missing audio/devices, repeated playback, interruption, and restoration using simulated devices. Build wheel/source archive and install into an empty environment. Run validate, preview, and simulate outside the checkout.

Live tests require configured speakers/lights and an audio backend; record those separately with device/firmware and OS versions. No live test should be inferred from a passing simulation.

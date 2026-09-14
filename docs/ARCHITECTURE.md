# Architecture

The starter validates configuration and translates cues into Light Show Manager events. GoveeClient handles devices; SimulatedTransport provides offline state. Pre-show captures all participating devices; post-show stops audio and attempts restoration for every captured device, aggregating errors. Audio uses an owned afplay/aplay subprocess.

Dependencies are pinned to merged source revisions pending separate package-registry publication. No code is copied from sibling checkouts. Original tones are distributed as package data.

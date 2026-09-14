import asyncio
import json
import math
from pathlib import Path
import shutil
from lightshow import LightShowManager, Show
from govee_lan_api_plus import GoveeClient, Profile


def load(path):
    path = Path(path)
    config = json.loads(path.read_text())
    if config.get('version') != 1 or not isinstance(config.get('name'), str):
        raise ValueError('Expected version 1 and a show name')
    duration = config.get('duration')
    if not isinstance(duration, (int, float)) or not math.isfinite(duration) or duration <= 0:
        raise ValueError('Duration must be positive and finite')
    roles = config.get('roles')
    if not isinstance(roles, dict) or not roles or not all(isinstance(v, str) for v in roles.values()):
        raise ValueError('Map logical roles to device IDs')
    cues = config.get('cues')
    if not isinstance(cues, list) or not cues:
        raise ValueError('At least one cue is required')
    for cue in cues:
        at = cue.get('at')
        if not isinstance(at, (int, float)) or not math.isfinite(at) or not 0 <= at <= duration:
            raise ValueError('Cue timestamp outside show duration')
        if cue.get('role') not in roles:
            raise ValueError('Cue references an unmapped role')
        action, value = cue.get('action'), cue.get('value')
        if action == 'brightness':
            valid = type(value) is int and 0 <= value <= 100
        elif action == 'color':
            valid = isinstance(value, list) and len(value) == 3 and all(type(v) is int and 0 <= v <= 255 for v in value)
        elif action == 'power':
            valid = isinstance(value, bool)
        elif action == 'scene':
            valid = isinstance(value, str) and bool(value)
        else:
            valid = False
        if not valid:
            raise ValueError(f'Invalid {action} cue value')
    if config.get('audio'):
        audio = (path.parent / config['audio']).resolve()
        if not audio.is_file():
            raise ValueError(f'Missing audio: {audio}')
        config['audio'] = str(audio)
    return config


async def play(config, client: GoveeClient, profile: Profile, simulate=True):
    devices = profile.devices or await client.discover()
    by_id = {d.id: d for d in devices}
    missing = set(config['roles'].values()) - by_id.keys()
    if missing:
        raise ValueError(f'Missing devices: {sorted(missing)}')
    scenes = {s.name: s for s in profile.scenes}
    if any(c['action'] == 'scene' and c['value'] not in scenes for c in config['cues']):
        raise ValueError('A referenced scene is missing from the profile')
    backend = None
    if config.get('audio') and not simulate:
        backend = shutil.which('afplay') or shutil.which('aplay')
        if not backend:
            raise ValueError('Install afplay (macOS) or aplay (Linux) for live audio, or omit audio')
    snapshots = {}
    process = None
    async def before(show, context):
        nonlocal process
        # Snapshot every participating device before changing any of them.
        for identifier in set(config['roles'].values()):
            snapshots[identifier] = await client.status(by_id[identifier])
        if backend:
            process = await asyncio.create_subprocess_exec(backend, config['audio'], stdout=asyncio.subprocess.DEVNULL, stderr=asyncio.subprocess.PIPE)
        elif config.get('audio'):
            print('Audio: simulated original spell tones')
    async def after(show, context):
        errors = []
        if process and process.returncode is None:
            process.terminate()
            try:
                await asyncio.wait_for(process.wait(), 2)
            except asyncio.TimeoutError:
                process.kill()
                await process.wait()
        for identifier, state in snapshots.items():
            try:
                await client.restore(by_id[identifier], state)
            except Exception as error:
                errors.append(error)
        if errors:
            raise ExceptionGroup('Device restoration failed', errors)
        print('Device state restored')
    async def execute(cue):
        device = by_id[config['roles'][cue['role']]]
        action, value = cue['action'], cue['value']
        print(f"{cue['at']:5.2f}s {cue['role']}: {action} {value}")
        if action == 'color':
            await client.color(device, *value)
        elif action == 'brightness':
            await client.brightness(device, value)
        elif action == 'power':
            await client.power(device, value)
        else:
            await client.scene(device, scenes[value])
    show = Show(config['name'], config['duration'])
    for cue in config['cues']:
        show.add_async_event(cue['at'], lambda cue=cue: execute(cue))
    async with LightShowManager([show], pre_show=before, post_show=after) as manager:
        return await manager.run_show(show.name)

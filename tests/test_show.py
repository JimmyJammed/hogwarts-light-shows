import asyncio
from importlib.resources import files
import json
import pytest
from govee_lan_api_plus import GoveeClient, Profile, SimulatedTransport
from hogwarts_light_shows.show import load, play


def sample():
    return load(files('hogwarts_light_shows').joinpath('assets/lanterns.json'))

@pytest.mark.asyncio
async def test_repeat_restores():
    config=sample();config['duration']=.01;config['cues']=[dict(config['cues'][0],at=0)]
    client=GoveeClient(SimulatedTransport())
    device=(await client.discover())[0]
    original=await client.status(device)
    for _ in range(2):
        assert (await play(config,client,Profile())).status == 'completed'
        assert await client.status(device) == original

@pytest.mark.asyncio
async def test_interrupt_restores():
    client=GoveeClient(SimulatedTransport())
    task=asyncio.create_task(play(sample(),client,Profile()))
    await asyncio.sleep(.03)
    task.cancel()
    with pytest.raises(asyncio.CancelledError): await task
    device=(await client.discover())[0]
    assert (await client.status(device))['brightness'] == 25

@pytest.mark.asyncio
async def test_missing_device_rejected():
    with pytest.raises(ValueError,match='Missing devices'):
        await play(sample(),GoveeClient(SimulatedTransport([])),Profile())

@pytest.mark.parametrize('change', ['time','role','audio','brightness'])
def test_invalid_config(tmp_path,change):
    config=sample();config.pop('audio',None)
    if change=='time':config['cues'][0]['at']=-1
    if change=='role':config['cues'][0]['role']='missing'
    if change=='audio':config['audio']='missing.wav'
    if change=='brightness':config['cues'][0].update(action='brightness',value=101)
    path=tmp_path/'show.json';path.write_text(json.dumps(config))
    with pytest.raises(ValueError):load(path)

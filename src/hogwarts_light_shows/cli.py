import argparse
import asyncio
from importlib.resources import files
from govee_lan_api_plus import GoveeClient, Profile, SimulatedTransport, Device, GoveeError
from .show import load, play


def main():
    parser = argparse.ArgumentParser(description='Wizard-themed show starter; simulation is default')
    parser.add_argument('command', choices=['validate', 'preview', 'simulate', 'run'])
    parser.add_argument('--show', default=str(files('hogwarts_light_shows').joinpath('assets/lanterns.json')))
    parser.add_argument('--profile')
    args = parser.parse_args()
    try:
        config = load(args.show)
        profile = Profile.load(args.profile) if args.profile else Profile()
        if args.command == 'validate':
            print(f"Valid: {config['name']} ({len(config['cues'])} cues)")
        elif args.command == 'preview':
            print(config['name'])
            for cue in sorted(config['cues'], key=lambda c:c['at']):
                print(f"{cue['at']:5.2f}s | {cue['role']} | {cue['action']} {cue['value']}")
        else:
            simulated = args.command != 'run'
            if not simulated and not args.profile:
                raise ValueError('Live run requires --profile with discovered devices')
            transport = SimulatedTransport(profile.devices or [Device(v,'SIMULATED','127.0.0.1',k) for k,v in config['roles'].items()]) if simulated else None
            result = asyncio.run(play(config, GoveeClient(transport), profile, simulate=simulated))
            print(result.status)
    except (ValueError, OSError, GoveeError, ExceptionGroup) as error:
        parser.exit(1, f'{error}\n')


if __name__ == '__main__':
    main()

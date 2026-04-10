# steelseries_chatmix_fix

Got really fucking fed up with SteelSeries GG randomly deciding to ignore your physical ChatMix dial? Yeah, same.

To be absolutely clear: **You still need SteelSeries GG installed and running for this to work.** We still need its "Sonar - Gaming" and "Sonar - Chat" virtual audio cables to exist. This script is simply a lightweight, zero-bullshit Python workaround for when GG drops the ball. It reads your headset's physical dial directly and forces Windows to adjust the Sonar audio channels, completely bypassing GG's broken event handling.

## Installing
> You need **Python >=3.11** to use this script.

Install by using one of the following commands:
- `pip install .`
- `uv sync`

> [!NOTE]
> Depending on your Windows environment, you might also need the `hidapi` DLL installed on your system for the HID module to work.

## Usage
1. Make sure SteelSeries Sonar is running (we still need those virtual devices active).
2. Run the script with one of the following methods:
  - `python index.py` (usually debug)
  - `start.bat` (production)

## Supported devices/systems
I have mostly a **Arctis Nova Pro Wireless** running on Windows 11 Home, if it works somewhere else, good. I have this primarily working on my own machine, but pushed code for fun so I don't lose it.

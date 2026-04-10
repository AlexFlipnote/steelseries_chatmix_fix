import hid
import time
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL

STEELSERIES_VID = 0x1038
CHATMIX_REPORT_ID = 7
CHATMIX_EVENT_ID = 69


def get_sonar_volume_controls():
    """Find IAudioEndpointVolume interfaces for Sonar Gaming and Chat devices."""
    gaming_vol = None
    chat_vol = None

    for device in AudioUtilities.GetAllDevices():
        name = device.FriendlyName or ""
        if "Sonar - Gaming" in name or "Sonar - Game" in name:
            interface = device._dev.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            gaming_vol = interface.QueryInterface(IAudioEndpointVolume)
        elif "Sonar - Chat" in name:
            interface = device._dev.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            chat_vol = interface.QueryInterface(IAudioEndpointVolume)

    return gaming_vol, chat_vol


def find_chatmix_path() -> bytes | None:
    """Find the HID interface path that reports ChatMix events."""
    for device_dict in hid.enumerate(STEELSERIES_VID, 0):
        path = device_dict["path"]
        device = hid.device()
        try:
            device.open_path(path)
            device.set_nonblocking(1)
            deadline = time.time() + 0.1
            while time.time() < deadline:
                data = device.read(64)
                if data and data[0] == CHATMIX_REPORT_ID and data[1] == CHATMIX_EVENT_ID:
                    return path
        except Exception:
            pass
        finally:
            device.close()
    return None


def read_chatmix():
    print("Looking for Sonar audio devices...")
    gaming_vol, chat_vol = get_sonar_volume_controls()

    if not gaming_vol or not chat_vol:
        missing = []
        if not gaming_vol:
            missing.append("Sonar - Gaming")
        if not chat_vol:
            missing.append("Sonar - Chat")
        print(f"Could not find: {', '.join(missing)}")
        print("Make sure SteelSeries Sonar is running.")
        return

    print("Found Sonar devices.")
    print("Searching for ChatMix interface (spin the dial)...")

    path = None
    while path is None:
        path = find_chatmix_path()
        if path is None:
            time.sleep(0.2)

    print("Ready. Spin the ChatMix dial. (Ctrl+C to stop)\n")

    device = hid.device()
    try:
        device.open_path(path)
        device.set_nonblocking(1)

        while True:
            data = device.read(64)
            if data and data[0] == CHATMIX_REPORT_ID and data[1] == CHATMIX_EVENT_ID:
                game = data[2] / 100.0
                chat = data[3] / 100.0
                gaming_vol.SetMasterVolumeLevelScalar(game, None)
                chat_vol.SetMasterVolumeLevelScalar(chat, None)
                print(f"Game: {data[2]:3}%  Chat: {data[3]:3}%")
            time.sleep(0.05)

    except IOError as e:
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        device.close()


read_chatmix()

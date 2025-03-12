import os
import json
from pypresence import Presence
import time

def load_config():
    config_path = "cfg"
    config_file = os.path.join(config_path, "rpc_config.json")

    if not os.path.exists(config_path):
        os.makedirs(config_path)

    if os.path.exists(config_file):
        with open(config_file, "r") as file:
            return json.load(file)
    return {}

def save_config(config):
    config_path = "config"
    config_file = os.path.join(config_path, "rpc_config.json")

    with open(config_file, "w") as file:
        json.dump(config, file, indent=4)

def start_RPC():
    try:
        config = load_config()

        print("Choose your Discord client:")
        print("1. Discord (Stable)")
        print("2. Discord Canary")
        print("3. Discord PTB")
        client_choice = input("Enter the corresponding number (1/2/3): ").strip()

        if client_choice == "1":
            rpc_endpoint = "https://discord.com/api"
        elif client_choice == "2":
            rpc_endpoint = "https://canary.discord.com/api"
        elif client_choice == "3":
            rpc_endpoint = "https://ptb.discord.com/api"
        else:
            print("Invalid choice. Defaulting to Discord Stable.")
            rpc_endpoint = "https://discord.com/api"

        app_id = input(f"Discord application ID [{config.get('app_id', '')}]: ").strip() or config.get('app_id', '')
        large_image = input(f"Image name (icon) [{config.get('large_image', '')}]: ").strip() or config.get('large_image', '')
        large_text = input(f"Image text [{config.get('large_text', '')}]: ").strip() or config.get('large_text', '')
        details = input(f"Details [{config.get('details', '')}]: ").strip() or config.get('details', '')
        state = input(f"State [{config.get('state', '')}]: ").strip() or config.get('state', '')
        start_time = int(time.time()) - int(input("Elapsed time in seconds (0 for now): ") or config.get('start_time_offset', 0))

        buttons = []
        for i in range(2):
            label = input(f"Button {i + 1} text [{config.get(f'button_{i+1}_label', '')}] (leave empty to ignore): ").strip()
            if label:
                url = input(f"Button {i + 1} URL [{config.get(f'button_{i+1}_url', '')}]: ").strip() or config.get(f'button_{i+1}_url', '')
                buttons.append({"label": label, "url": url})

        save_choice = input("Do you want to save this configuration? (y/n): ").strip().lower()
        if save_choice == 'y':
            config.update({
                "app_id": app_id,
                "large_image": large_image,
                "large_text": large_text,
                "details": details,
                "state": state,
                "start_time_offset": time.time() - start_time
            })
            for i, button in enumerate(buttons):
                config[f"button_{i+1}_label"] = button["label"]
                config[f"button_{i+1}_url"] = button["url"]
            save_config(config)

        RPC = Presence(app_id, rpc_endpoint=rpc_endpoint)
        RPC.connect()

        print("\nRPC started. Press Ctrl+C to stop.")

        while True:
            try:
                RPC.update(
                    large_image=large_image,
                    large_text=large_text,
                    details=details,
                    state=state,
                    start=start_time,
                    buttons=buttons
                )
                time.sleep(3)
            except KeyboardInterrupt:
                print("\nStopped.")
                break
            except Exception as e:
                print(f"Error: {e}")
                break
    except Exception as e:
        print(f"Error: {e}")
    finally:
        try:
            RPC.close()
            print("Disconnected.")
        except:
            pass

if __name__ == "__main__":
    start_RPC()

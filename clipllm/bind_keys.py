import subprocess
import os
from pathlib import Path

def main():
    # Define your bindings here
    bindings = """
"clip-llm -r"
    m:0x15 + c:54
    Control+Shift+Mod2 + c
"clip-llm -s"
    m:0x1d + c:54
    Control+Shift+Alt+Mod2 + c
    """.strip()
    temp_filepath = Path('/home/jaime/.xbindkeysrc')
    # Create a temporary file for xbindkeys configuration
    with temp_filepath.open('w') as tmpfile:
        tmpfile.write(bindings)

    
    # Execute xbindkeys with the temporary file
    try:
        subprocess.run(['xbindkeys', '-f', temp_filepath], check=True)
        print("Hotkeys configured successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error configuring hotkeys: {e}")


if __name__ == "__main__":
    main()


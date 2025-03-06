import subprocess

def main():
    # .xbidkeyssrc
    subprocess.run(['xbindkeys', '-f', '.xbidkeyssrc'])
    print("Hotkeys configured successfully!")
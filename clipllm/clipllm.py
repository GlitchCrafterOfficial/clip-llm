from argparse import ArgumentParser
import os

def main():
    parser = ArgumentParser()
    parser.add_argument('-s', '--settings', action='store_true', help='Ejecuta src/settings.py')
    parser.add_argument('-i', '--init', action='store_true', help='Ejecuta src/bind_keys.py')
    parser.add_argument('-r', '--run', action='store_true', help='Ejecuta src/main_windows.py o src/main_linux.py')

    args = parser.parse_args()

    if args.settings:
        from src.settings import main as settings_main
        settings_main()
    if args.init:
        from src.bind_keys import main as bind_keys_main
        bind_keys_main()
    if args.run:
        if os.name == 'nt':
            from src.main_windows import main as main_windows_main
            main_windows_main()
        else:
            from src.main_linux import main as main_linux_main
            main_linux_main()


if __name__ == "__main__":
    main()
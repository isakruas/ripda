import os
import sys


def main():
    os.environ.setdefault('RIPDA_SETTINGS_MODULE', 'settings')
    try:
        from ripda.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Ripda"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

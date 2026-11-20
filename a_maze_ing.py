import sys
from app.config import ConfigError, parse_config


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: python3 {sys.argv[0]} <config_file>", file=sys.stderr)
        return 1

    try:
        config = parse_config(sys.argv[1])
        print(config)
        return 0
    except ConfigError as e:
        print(f"{e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())

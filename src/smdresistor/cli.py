import argparse
from .decoder import decode, format_ohms


def main(argv=None):
    parser = argparse.ArgumentParser(description="Decode SMD resistor codes")
    parser.add_argument("code", nargs="?", help="SMD code, e.g., 103, 4R7, 01C")
    parser.add_argument("--code", dest="code_kw", help="SMD code (alternative)")
    ns = parser.parse_args(argv)
    code = ns.code_kw or ns.code
    if not code:
        parser.error("please provide a code")
    try:
        result = decode(code)
        print(f"{code} => {format_ohms(result.ohms)} ({result.scheme})")
    except Exception as e:
        print(f"Error: {e}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


import argparse
from pathlib import Path
import sys

from . import __version__
from .checks import check_product
from .doctor import check_environment


PRODUCT_TYPES = ("prompt-pack", "xlsx", "ebook")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m product_qa",
        description="Product QA Gate for offline digital-product checks.",
    )
    parser.add_argument("--version", action="version", version=__version__)
    commands = parser.add_subparsers(dest="command")
    check = commands.add_parser("check", help="run universal product checks")
    check.add_argument("product_path")
    check.add_argument("--type", choices=PRODUCT_TYPES, required=True)
    check.add_argument("--json-out", type=Path, required=True)
    commands.add_parser("doctor", help="check local validation tools")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    arguments = parser.parse_args(argv)
    if arguments.command is None:
        parser.print_help()
        return 0

    if arguments.command == "doctor":
        report = check_environment()
        print(report.to_human())
        return report.exit_code

    output_error = _output_error(arguments.product_path, arguments.json_out)
    if output_error:
        parser.error(output_error)

    report = check_product(arguments.product_path, arguments.type)
    print(report.to_human())
    try:
        with arguments.json_out.open("x", encoding="utf-8") as report_file:
            report_file.write(report.to_json())
    except OSError:
        print("Cannot write JSON report.", file=sys.stderr)
        return 2
    return report.exit_code


def _output_error(product_path: str, output: Path) -> str | None:
    try:
        if output.is_symlink() or output.exists():
            return "--json-out must name a new regular file"
        if not output.parent.is_dir():
            return "--json-out parent directory does not exist"
        product = Path(product_path)
        if product.exists():
            root = product.resolve(strict=True)
            root = root if root.is_dir() else root.parent
            try:
                output.resolve().relative_to(root)
            except ValueError:
                return None
            return "--json-out must be outside the product path"
    except (OSError, ValueError):
        return "--json-out path cannot be used"
    return None


if __name__ == "__main__":
    raise SystemExit(main())

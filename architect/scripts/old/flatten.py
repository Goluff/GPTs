import yaml
import sys
from pathlib import Path

def parse_args():
    import argparse
    parser = argparse.ArgumentParser(description="Flatten a multi-doc YAML file into a single list")
    parser.add_argument("input", help="Path to the input YAML file (multi-doc)")
    parser.add_argument("output", nargs="?", help="Path to the output file (optional if --in-place is used)")
    parser.add_argument("--in-place", action="store_true", help="Replace input file with flattened version")
    return parser.parse_args()

class IndentDumper(yaml.Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super().increase_indent(flow, False)

def main():
    args = parse_args()

    input_path = Path(args.input)
    output_path = input_path if args.in_place else Path(args.output)

    if not input_path.exists():
        print(f"❌ Error: {input_path} does not exist.")
        sys.exit(1)

    with input_path.open("r", encoding="utf-8") as f:
        documents = list(yaml.safe_load_all(f))

    documents.sort(key=lambda d: d.get("id", ""))

    with output_path.open("w", encoding="utf-8") as f:
        f.write("---\n")
        yaml.dump(
            documents,
            f,
            Dumper=IndentDumper,
            allow_unicode=True,
            default_flow_style=False,
            indent=2,
            sort_keys=False,
            width=88,
        )

    print(f"✅ Flattened YAML written to: {output_path}")

if __name__ == "__main__":
    main()

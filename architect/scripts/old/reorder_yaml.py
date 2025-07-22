import sys
import json
import yaml
from yaml import Dumper
from collections import OrderedDict

class IndentDumper(Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super().increase_indent(flow, False)

def load_schema_order(schema_path):
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)
    return list(schema.get("properties", {}).keys())

def reorder_dict(data, order):
    if not isinstance(data, dict):
        return data
    ordered = OrderedDict()
    for key in order:
        if key in data:
            ordered[key] = data[key]
    for key in data:
        if key not in ordered:
            ordered[key] = data[key]
    return ordered

def reorder_yaml(data, order):
    if isinstance(data, list):
        return [reorder_dict(item, order) for item in data]
    elif isinstance(data, dict):
        return reorder_dict(data, order)
    return data

def strip_ordered_dict(obj):
    if isinstance(obj, OrderedDict):
        return {k: strip_ordered_dict(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [strip_ordered_dict(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: strip_ordered_dict(v) for k, v in obj.items()}
    else:
        return obj

def main(yaml_path, schema_path, output_path):
    with open(yaml_path, "r", encoding="utf-8") as f:
        data = yaml.load(f, Loader=yaml.Loader)  # attention : potentiellement non-safe

    order = load_schema_order(schema_path)
    data_ordered = reorder_yaml(data, order)
    data_clean = strip_ordered_dict(data_ordered)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("---\n")
        yaml.dump(
            data_clean,
            f,
            Dumper=IndentDumper,
            allow_unicode=True,
            default_flow_style=False,
            sort_keys=False
        )

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python reorder_yaml.py input.yaml schema.json output.yaml")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2], sys.argv[3])

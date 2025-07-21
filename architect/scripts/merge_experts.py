#!/usr/bin/env python3

import os
import yaml
import glob
import copy

from yaml.dumper import Dumper

# Custom YAML dumper for clean indentation
class IndentDumper(Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super().increase_indent(flow, False)

# Global string presenter: plain style unless quoting is required
def str_presenter(dumper, data):
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='')  # plain

yaml.add_representer(str, str_presenter)

# Load YAML with UTF-8
def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

# Write YAML with UTF-8 and correct formatting
def write_yaml(data, path):
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, sort_keys=False, explicit_start=True, Dumper=IndentDumper)

# Render template with strict tag enforcement
def render_template(template: str, expert: dict, source_path: str) -> str:
    output = template
    for key in ["name", "title", "domain", "tone", "style_language", "behavior_model"]:
        if key not in expert:
            raise ValueError(f"Missing field '{key}' in expert '{expert.get('id')}' from {source_path}")
        output = output.replace("{{" + key + "}}", expert[key])
    return " ".join(output.strip().split())  # collapse whitespace and newlines

def main():
    # Load master files
    ethics_files = glob.glob("ethics/**/*.yaml", recursive=True)
    expert_files = glob.glob("experts/**/*.yaml", recursive=True)
    instructions = load_yaml("persona/instructions.yaml")["instructions"]
    persona_assertions = load_yaml("persona/persona-assertions.yaml")["persona_assertions"]

    # Build ethics index
    ethics_map = {}
    for path in ethics_files:
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            if not data:
                continue
            for item in data:
                eid = item["id"]
                ethics_copy = copy.deepcopy(item)
                ethics_copy.pop("id", None)
                ethics_map[eid] = ethics_copy

    merged_experts = []
    missing_ethics = []

    for path in expert_files:
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            if not data:
                continue
            for expert in data:
                eid = expert.get("id")

                # Inject ethics
                if eid and eid in ethics_map:
                    expert["ethics"] = ethics_map[eid]
                else:
                    print(f"\033[33m⚠️   Missing ethics block for expert '{eid}'\033[0m")
                    expert["ethics"] = {"note": "No ethics block found for this expert."}
                    missing_ethics.append(eid)

                # Inject persona assertions
                expert["persona_assertions"] = copy.deepcopy(persona_assertions)

                # Render instructions
                rendered = {}
                for k, v in instructions.items():
                    rendered[k] = render_template(v, expert, source_path=path)
                expert["instructions"] = rendered

                # Remove rendered behavior keys
                for key in ["tone", "style_language", "behavior_model"]:
                    expert.pop(key, None)

                merged_experts.append(expert)

    # Output merged expert file
    os.makedirs("build", exist_ok=True)
    output_path = "build/experts.yaml"
    write_yaml(merged_experts, output_path)

    print(f"\033[32m✅ Experts merged → {output_path}\033[0m")
    if missing_ethics:
        print(f"\033[33m⚠️   {len(missing_ethics)} expert(s) missing ethics – review above warnings.\033[0m")

if __name__ == "__main__":
    main()

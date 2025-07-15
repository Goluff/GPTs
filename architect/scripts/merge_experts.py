#!/usr/bin/env python3

import os
import yaml
import glob
import copy

def collect_yaml_entries(patterns):
    entries = []
    for pattern in patterns:
        for path in glob.glob(pattern, recursive=True):
            with open(path, 'r') as f:
                data = yaml.safe_load(f)
                if data:
                    entries.extend(data)
    return entries

def main():
    ethics_files = glob.glob("ethics/**/*.yaml", recursive=True)
    expert_files = glob.glob("experts/**/*.yaml", recursive=True)

    # Index ethics by ID
    ethics_map = {}
    for path in ethics_files:
        with open(path, 'r') as f:
            data = yaml.safe_load(f)
            if not data:
                continue
            for item in data:
                ethics_id = item["id"]
                ethics_copy = copy.deepcopy(item)
                ethics_copy.pop("id", None)
                ethics_map[ethics_id] = ethics_copy

    # Merge ethics into experts
    merged_experts = []
    missing_ethics = []
    for path in expert_files:
        with open(path, 'r') as f:
            data = yaml.safe_load(f)
            if not data:
                continue
            for expert in data:
                eid = expert.get("ethics")
                if eid and eid in ethics_map:
                    expert["ethics"] = ethics_map[eid]
                elif eid:
                    print(f"\033[33m   Missing ethics block for expert '{expert.get('id', 'unknown')}' → {eid}\033[0m")
                    expert["ethics"] = {"note": f"Unresolved ethics ID: {eid}"}
                    missing_ethics.append(expert.get('id', 'unknown'))
                else:
                    print(f"\033[33m   No ethics ID defined for expert '{expert.get('id', 'unknown')}'\033[0m")
                    missing_ethics.append(expert.get('id', 'unknown'))
                merged_experts.append(expert)

    # Write output
    os.makedirs("build", exist_ok=True)
    output_path = "build/experts.yaml"
    with open(output_path, "w") as f:
        yaml.dump(merged_experts, f, sort_keys=False)

    print(f"\033[32m   Ethics injected → {output_path}\033[0m")
    if missing_ethics:
        print(f"\033[33m   {len(missing_ethics)} expert(s) missing ethics – review above warnings.\033[0m")

if __name__ == "__main__":
    main()

import yaml
import os
from yaml.dumper import Dumper

# Custom dumper for consistent indentation
class IndentDumper(Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super().increase_indent(flow, False)

# Utility to load YAML
def load_yaml(path):
    with open(path, 'r') as f:
        return yaml.safe_load(f)

# Utility to write YAML with document start and custom indentation
def write_yaml(data, path):
    with open(path, 'w') as f:
        yaml.dump(data, f, sort_keys=False, explicit_start=True, Dumper=IndentDumper)

# Load inputs
fields = load_yaml("fields.yaml")
experts = load_yaml("experts/experts.yaml")
indexes = load_yaml("indexes/experts-index.yaml")
ethics = load_yaml("ethics/ethics.yaml")

# Prepare ID lookup maps
experts_by_id = {item['id']: item for item in experts}
indexes_by_id = {item['id']: item for item in indexes}
ethics_by_id = {item['id']: item for item in ethics}

# Extract acronym and expert groups
acronym_to_field = fields["expert_fields"]
field_to_ids = {field: ids for field, ids in fields.items() if field != "expert_fields"}

# Ensure output directories exist
os.makedirs("experts", exist_ok=True)
os.makedirs("indexes", exist_ok=True)
os.makedirs("ethics", exist_ok=True)

# Process each field
for acronym, field in acronym_to_field.items():
    ids = field_to_ids.get(field, [])

    expert_out = [experts_by_id[i] for i in ids if i in experts_by_id]
    index_out = [indexes_by_id[i] for i in ids if i in indexes_by_id]
    ethics_out = [ethics_by_id[i] for i in ids if i in ethics_by_id]

    write_yaml(expert_out, f"experts/experts-{acronym}.yaml")
    write_yaml(index_out, f"indexes/experts-index-{acronym}.yaml")
    write_yaml(ethics_out, f"ethics/ethics-{acronym}.yaml")


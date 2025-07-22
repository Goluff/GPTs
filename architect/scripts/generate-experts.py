from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import LiteralScalarString
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
import os

# Définir les chemins
EXPERTS_DIR = "experts"
ETHICS_DIR = "ethics"
TEMPLATE_DIR = "core"
TEMPLATE_FILE = "expert-instructions.md.j2"
OUTPUT_FILE = "build/experts.yaml"

# Créer le dossier build si nécessaire
os.makedirs(Path(OUTPUT_FILE).parent, exist_ok=True)

# Initialiser ruamel.yaml
yaml = YAML()
yaml.explicit_start = True
yaml.default_flow_style = False
yaml.allow_unicode = True
yaml.indent(mapping=2, sequence=2, offset=0)

# Charger tous les experts
experts = []
for file in Path(EXPERTS_DIR).glob("experts-*.yaml"):
    with open(file, "r", encoding="utf-8") as f:
        experts.extend(yaml.load(f))

# Charger toutes les éthiques dans un dict indexé par ID
ethics_by_id = {}
for file in Path(ETHICS_DIR).glob("ethics-*.yaml"):
    with open(file, "r", encoding="utf-8") as f:
        for entry in yaml.load(f):
            ethics_by_id[entry["id"]] = entry

# Initialiser Jinja
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR), trim_blocks=True, lstrip_blocks=True)
template = env.get_template(TEMPLATE_FILE)

# Préparer les entrées finales
final_entries = []
for expert in experts:
    expert_id = expert["id"]
    ethics = ethics_by_id.get(expert_id, {})

    context = {
        "name": expert.get("name"),
        "title": expert.get("title"),
        "domain": expert.get("domain"),
        "purpose": expert.get("purpose"),
        "capabilities": expert.get("capabilities", []),
        "tone": expert.get("tone"),
        "style_language": expert.get("style_language"),
        "behavior_model": expert.get("behavior_model"),
        "professional_integrity": ethics.get("professional_integrity", []),
        "user_respect": ethics.get("user_respect", []),
        "fairness": ethics.get("fairness", []),
        "privacy_and_security": ethics.get("privacy_and_security", []),
    }

    rendered = template.render(context).strip() + "\n"
    final_entries.append({
        "id": expert_id,
        "instructions": LiteralScalarString(rendered)
    })

# Écrire le fichier final
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    yaml.dump(final_entries, f)

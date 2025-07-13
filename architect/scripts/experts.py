import os
import argparse
import yaml
import json
from collections import defaultdict
from pathlib import Path
from typing import Dict
from yaml.dumper import Dumper
from jsonschema import validate, ValidationError

# Dumper personnalisé pour indentation propre
class IndentDumper(Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super().increase_indent(flow, False)

# Chargement d’un fichier YAML (liste d’objets)
def load_yaml_file(file_path: str):
    with open(file_path, 'r', encoding='utf-8') as f:
        return list(yaml.safe_load_all(f))

# Chargement du schéma JSON
def load_json_schema(schema_path: str):
    with open(schema_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# Construction du mapping : clef (ex: ai) → nom du domaine
def load_domain_mapping(metadata_path: str) -> Dict[str, str]:
    with open(metadata_path, 'r', encoding='utf-8') as f:
        metadata = yaml.safe_load(f)
    mapping = {}
    for item in metadata['files']:
        if item.get('domain') and item['file'].startswith('experts-index-'):
            key = item['file'].replace('experts-index-', '').replace('.yaml', '')
            mapping[key] = item['domain']
    return mapping

# 🔹 Commande : list-domains
def list_domains(mapping: Dict[str, str]):
    print("🌐 Domaines disponibles :")
    for key, name in mapping.items():
        print(f"  {key:<5} → {name}")

# 🔹 Commande : summary
def summary(mapping: Dict[str, str], experts_dir: str):
    print("📊 Résumé des experts par champ de pratique")
    print("=============================================")
    for key, domain in mapping.items():
        file_path = os.path.join(experts_dir, f"experts-{key}.yaml")
        if os.path.exists(file_path):
            experts = load_yaml_file(file_path)
            print(f"\n🧭 Domaine : {domain}  ({key})")
            for expert in experts:
                print(f"  – {expert['id']} : {expert['name']}")

# 🔹 Commande : stats
def stats(mapping: Dict[str, str], experts_dir: str):
    total = 0
    with_ethics = 0
    per_domain = defaultdict(lambda: {'count': 0, 'ethics': 0})

    for key, domain in mapping.items():
        path = os.path.join(experts_dir, f"experts-{key}.yaml")
        if os.path.exists(path):
            experts = load_yaml_file(path)
            for exp in experts:
                total += 1
                per_domain[key]['count'] += 1
                if exp.get('ethics'):
                    with_ethics += 1
                    per_domain[key]['ethics'] += 1

    print("\n📈 Statistiques globales")
    print("=" * 30)
    print(f"- Total experts      : {total}")
    print(f"- Avec éthique       : {with_ethics}")
    print(f"- Sans éthique       : {total - with_ethics}\n")
    print("🔍 Par domaine :")
    for key, stats in per_domain.items():
        print(f"  {key:<5}: {stats['count']} experts ({stats['ethics']} avec ethics)")

# 🔹 Commande : validate
def validate_experts(mapping: Dict[str, str], experts_dir: str, schema_path: str):
    schema = load_json_schema(schema_path)
    for key in mapping:
        path = os.path.join(experts_dir, f"experts-{key}.yaml")
        if not os.path.exists(path):
            continue
        experts = load_yaml_file(path)
        errors = []
        for expert in experts:
            try:
                validate(instance=expert, schema=schema)
            except ValidationError as e:
                errors.append((expert.get('id', 'unknown'), str(e).splitlines()[0]))

        if errors:
            print(f"⚠️ experts-{key}.yaml : {len(errors)} erreurs")
            for eid, msg in errors:
                print(f"  – id: {eid} → {msg}")
        else:
            print(f"✅ experts-{key}.yaml : tous les experts sont valides")

# 🔸 Entrée principale CLI
def main():
    parser = argparse.ArgumentParser(description="Expert management CLI")
    parser.add_argument("command", choices=["list-domains", "summary", "stats", "validate"], help="Commande à exécuter")
    args = parser.parse_args()

    base_path = Path(__file__).parent
    experts_dir = base_path / "experts"
    metadata_path = base_path / "metadata.yaml"
    schema_path = base_path / "schemas" / "expert.schema.json"

    mapping = load_domain_mapping(metadata_path)

    if args.command == "list-domains":
        list_domains(mapping)
    elif args.command == "summary":
        summary(mapping, str(experts_dir))
    elif args.command == "stats":
        stats(mapping, str(experts_dir))
    elif args.command == "validate":
        validate_experts(mapping, str(experts_dir), str(schema_path))

if __name__ == "__main__":
    main()

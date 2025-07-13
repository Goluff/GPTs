import sys
import yaml

class IndentDumper(yaml.Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super().increase_indent(flow, False)

def load_yaml_list(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
        if not isinstance(data, list):
            raise ValueError("Le fichier YAML ne contient pas une liste.")
        return data

def find_entries_by_id(entries, target_id):
    return [entry for entry in entries if isinstance(entry, dict) and entry.get('id') == target_id]

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python search_yaml.py <fichier.yaml> <id>")
        sys.exit(1)

    filename = sys.argv[1]
    search_id = sys.argv[2]

    try:
        items = load_yaml_list(filename)
        result = find_entries_by_id(items, search_id)
        if result:
            print(yaml.dump(result, Dumper=IndentDumper, sort_keys=False, allow_unicode=True, default_flow_style=False))
        else:
            print(f"Aucune entrée trouvée avec l’id '{search_id}'")
    except Exception as e:
        print(f"Erreur : {e}")
        sys.exit(1)

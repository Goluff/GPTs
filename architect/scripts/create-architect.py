from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap, CommentedSeq
from pathlib import Path
import os

# Définir les chemins
ARCHITECT_FILE = "core/the-architect.yaml"
BEHAVIOR_FILE = "core/behavior-flow.yaml"
OUTPUT_FILE = "build/the-architect.yaml"

# Créer le dossier build s'il n'existe pas
os.makedirs(Path(OUTPUT_FILE).parent, exist_ok=True)

# Initialiser YAML
yaml = YAML()
yaml.explicit_start = True
yaml.default_flow_style = False
yaml.indent(mapping=2, sequence=4, offset=2)

# Lire les fichiers source
with open(ARCHITECT_FILE, "r", encoding="utf-8") as f:
    architect = yaml.load(f)

with open(BEHAVIOR_FILE, "r", encoding="utf-8") as f:
    behavior = yaml.load(f)

# Fonction récursive pour enlever tous les commentaires
def strip_comments(obj):
    if isinstance(obj, CommentedSeq):
        return [strip_comments(i) for i in obj]
    elif isinstance(obj, CommentedMap):
        return {k: strip_comments(v) for k, v in obj.items()}
    else:
        return obj

# Nettoyage du bloc behavior_flow
behavior_flow_clean = strip_comments(behavior.get("behavior_flow"))

# Injection dans the_architect
architect["the_architect"]["behavior_flow"] = behavior_flow_clean

# Écriture du fichier final
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    yaml.dump(architect, f)

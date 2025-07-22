#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CLI tool for validating and summarizing YAML-based expert configurations."""

import json
from collections import defaultdict
from pathlib import Path
from typing import Dict

import typer
import yaml
from jsonschema import ValidationError, validate
from rich import box
from rich.console import Console
from rich.table import Table

app = typer.Typer(invoke_without_command=True)


@app.callback()
def main(ctx: typer.Context):
    """CLI tool for validating and summarizing YAML-based expert configurations."""
    if ctx.invoked_subcommand is None:
        typer.echo(ctx.get_help())
        raise typer.Exit()


console = Console()

# ════════════════════════════════════════════════════════════════
# 📁 CONFIGURATION – paths, constants, icons
# ════════════════════════════════════════════════════════════════

EXPERTS_DIR = Path("experts")
INDEXES_DIR = Path("indexes")
ETHICS_DIR = Path("ethics")
CORE_DIR = Path("core")
SCHEMAS_DIR = Path("schemas")
EXPERT_FILE = "experts-{key}.yaml"
INDEX_FILE = "experts-index-{key}.yaml"
ETHIC_FILE = "ethics-{key}.yaml"
METADATA_FILE = CORE_DIR / "metadata.yaml"
EXPERT_SCHEMA_FILE = SCHEMAS_DIR / "expert.schema.json"
INDEX_SCHEMA_FILE = SCHEMAS_DIR / "expert-index.schema.json"
ETHIC_SCHEMA_FILE = SCHEMAS_DIR / "ethic.schema.json"

ICONS = {
    "domain": "",
    "expert": "",
    "section": "",
    "stats": "",
    "valid": "",
    "warning": "",
    "error": "",
    "group": "",
    "check": "",
    "link": "",
    "ethic": "",
}


class IndentDumper(yaml.Dumper):
    """Public class."""

    def increase_indent(self, flow=False, indentless=False):
        """Public method."""
        return super().increase_indent(flow, False)


# ════════════════════════════════════════════════════════════════
# 📦 UTILS
# ════════════════════════════════════════════════════════════════


def load_yaml(file_path: Path):
    """Load a YAML file and return its contents as a Python object."""
    with open(file_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_json(schema_path: Path):
    """Load a JSON file and return its contents as a Python object."""
    with open(schema_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_domain_mapping(metadata_path: Path) -> Dict[str, str]:
    """Load the mapping of domain keys to domain names from the metadata YAML file."""
    with open(metadata_path, "r", encoding="utf-8") as f:
        metadata = yaml.safe_load(f)
    return metadata.get("expert_fields", {})

#def load_domain_mapping(metadata_path: Path) -> Dict[str, str]:
#    """Load the mapping of domain keys to domain names from the metadata YAML file."""
#    with open(metadata_path, "r", encoding="utf-8") as f:
#        metadata = yaml.safe_load(f)
#    mapping = {}
#    for item in metadata.get("files", []):
#        if item.get("domain") and item.get("file", "").startswith("experts-index-"):
#            key = item["file"].replace("experts-index-", "").replace(".yaml", "")
#            mapping[key] = item["domain"]
#    return mapping


def run_validation(
    schema_file: Path,
    directory: Path,
    pattern: str,
    category: str,
    quiet: bool = False,
) -> dict[Path, list[str]]:
    """Validate a set of YAML files in a directory against a JSON schema, optionally returning errors."""
    schema = load_json(schema_file)
    files = sorted(directory.glob(pattern))
    results = {}

    for file in files:
        try:
            data = load_yaml(file)
        except Exception as e:
            msg = f"{ICONS['error']} Failed to read {file.name}: {e}"
            if not quiet:
                console.print(f"[bold red]{msg}[/bold red]")
            results[file] = [msg]
            continue

        errors = []
        for entry in data if isinstance(data, list) else [data]:
            try:
                validate(instance=entry, schema=schema)
            except ValidationError as e:
                entry_id = entry.get("id", "?")
                msg = f"  – id: {entry_id} → {e.message.splitlines()[0]}"
                errors.append(msg)

        results[file] = errors

        if not quiet:
            if errors:
                console.print(
                    f"[yellow]{ICONS['warning']} {file.name}:[/yellow] {len(errors)} validation error(s)"
                )
                for err in errors:
                    console.print(err)
            else:
                console.print(
                    f"[green]{ICONS['valid']} {file.name}:[/green] all {category} are valid"
                )

    return results


def check_index_consistency(
    experts_dir: Path, indexes_dir: Path, metadata_file: Path, quiet: bool = False
) -> dict:
    """Check index consistency across all domains, returning counts of missing and orphan indexes."""
    domain_map = load_domain_mapping(metadata_file)
    summary = {}

    for key, domain in domain_map.items():
        expert_path = experts_dir / EXPERT_FILE.format(key=key)
        index_path = indexes_dir / INDEX_FILE.format(key=key)

        if not expert_path.exists() or not index_path.exists():
            continue

        experts = load_yaml(expert_path)
        indexes = load_yaml(index_path)

        expert_ids = {e["id"] for e in experts}
        expert_names = {e["id"]: e["name"] for e in experts}
        index_ids = {i["id"] for i in indexes}

        missing = expert_ids - index_ids
        orphans = index_ids - expert_ids

        summary[domain] = {"missing": len(missing), "orphans": len(orphans)}

        if not quiet:
            if not missing and not orphans:
                console.print(
                    f"[green]{ICONS['valid']} {domain}:[/green] All experts are indexed"
                )
            else:
                console.print(f"[yellow]{ICONS['warning']} {domain}:[/yellow]")
                for mid in sorted(missing):
                    name = expert_names.get(mid, mid)
                    console.print(
                        f"    [red]{ICONS['error']} Missing index for:[/red] {name}"
                    )
                for oid in sorted(orphans):
                    console.print(
                        f"    [red]{ICONS['error']} Orphan index:[/red] {oid}"
                    )

    return summary


def check_ethic_consistency(
    experts_dir: Path, ethics_dir: Path, metadata_file: Path, quiet: bool = False
) -> dict:
    """Check ethic consistency across all domains, returning counts of missing and orphan ethics."""
    domain_map = load_domain_mapping(metadata_file)
    summary = {}

    for key, domain in domain_map.items():
        expert_path = experts_dir / EXPERT_FILE.format(key=key)
        ethic_path = ethics_dir / ETHIC_FILE.format(key=key)

        if not expert_path.exists() or not ethic_path.exists():
            continue

        experts = load_yaml(expert_path)
        ethics = load_yaml(ethic_path)

        referenced_ids = {e["id"] for e in experts if "id" in e}
        ethic_ids = {e["id"] for e in ethics}

        missing = referenced_ids - ethic_ids
        orphans = ethic_ids - referenced_ids

        summary[domain] = {"missing": len(missing), "orphans": len(orphans)}

        if not quiet:
            if not missing and not orphans:
                console.print(
                    f"[green]{ICONS['valid']} {domain}:[/green] All ethics references are valid"
                )
            else:
                console.print(f"[yellow]{ICONS['warning']} {domain}:[/yellow]")
                for mid in sorted(missing):
                    console.print(
                        f"    [red]{ICONS['error']} Missing ethic rule:[/red] {mid}"
                    )
                for oid in sorted(orphans):
                    console.print(
                        f"    [red]{ICONS['error']} Orphan ethic entry:[/red] {oid}"
                    )

    return summary


# ════════════════════════════════════════════════════════════════
# ✅ COMMANDES
# ════════════════════════════════════════════════════════════════


@app.command("list-domains")
def list_domains():
    """Display the available domains loaded from metadata.yaml."""
    mapping = load_domain_mapping(METADATA_FILE)

    console.rule(f"{ICONS['domain']} Available domains", style="bold cyan")
    for key, name in mapping.items():
        console.print(f"  [cyan]{key:<5}[/cyan] → [green]{name}[/green]")


@app.command("summary")
def summary():
    """Print a summary of expert IDs and names grouped by domain."""
    mapping = load_domain_mapping(METADATA_FILE)
    experts_dir = EXPERTS_DIR

    console.rule(f"{ICONS['section']} Expert summary by domain", style="bold cyan")
    for key, domain in mapping.items():
        path = experts_dir / f"experts-{key}.yaml"
        if path.exists():
            experts = load_yaml(path)
            console.print(f"\n{ICONS['group']} [bold cyan]Domain:[/bold cyan] {domain}")
            for exp in experts:
                console.print(f"  – [bold]{exp['name']} - {exp['title']}")
        else:
            console.print(f"[red]Fichier manquant pour le domaine '{key}'[/red]")


@app.command("validate-experts")
def cli_validate_experts():
    """CLI command to validate expert files using expert.schema.json."""
    console.rule(
        f"{ICONS['check']} Validation of experts files with schema", style="bold cyan"
    )
    run_validation(EXPERT_SCHEMA_FILE, EXPERTS_DIR, "experts-*.yaml", "experts")


@app.command("validate-indexes")
def cli_validate_indexes():
    """CLI command to validate expert-index files using expert-index.schema.json."""
    console.rule(
        f"{ICONS['check']} Validation of indexes files with schema", style="bold cyan"
    )
    run_validation(INDEX_SCHEMA_FILE, INDEXES_DIR, "experts-index-*.yaml", "indexes")


@app.command("validate-ethics")
def cli_validate_ethics():
    """CLI command to validate ethics files using ethic.schema.json."""
    console.rule(
        f"{ICONS['check']} Validation of ethics files with schema", style="bold cyan"
    )
    run_validation(ETHIC_SCHEMA_FILE, ETHICS_DIR, "ethics-*.yaml", "ethics")


@app.command("check-indexes")
def cli_check_indexes():
    """Check that every expert has a corresponding index and that no orphan indexes exist."""
    console.rule(
        f"{ICONS['link']} Index consistency check across all domains", style="bold cyan"
    )
    check_index_consistency(EXPERTS_DIR, INDEXES_DIR, METADATA_FILE, quiet=False)


@app.command("check-ethics")
def cli_check_ethics():
    """Check that every expert has a corresponding ethic rule and that no orphan ethics exist."""
    console.rule(
        f"{ICONS['ethic']} Ethic consistency check across all domains",
        style="bold cyan",
    )
    check_ethic_consistency(EXPERTS_DIR, ETHICS_DIR, METADATA_FILE, quiet=False)


@app.command("validate")
def cli_validate_all():
    """Validate all expert, index, and ethics files and summarize non-conformities by domain."""
    console.rule(f"{ICONS['check']} Validation Summary by Domain", style="bold cyan")

    domain_map = load_domain_mapping(METADATA_FILE)
    domain_summary = defaultdict(
        lambda: {
            "experts": 0,
            "indexes": 0,
            "ethics": 0,
            "missing_indexes": 0,
            "orphan_indexes": 0,
            "missing_ethics": 0,
            "orphan_ethics": 0,
        }
    )

    for category, dir_path, schema_file, pattern in [
        ("experts", EXPERTS_DIR, EXPERT_SCHEMA_FILE, "experts-*.yaml"),
        ("indexes", INDEXES_DIR, INDEX_SCHEMA_FILE, "experts-index-*.yaml"),
        ("ethics", ETHICS_DIR, ETHIC_SCHEMA_FILE, "ethics-*.yaml"),
    ]:
        results = run_validation(
            schema_file=schema_file,
            directory=dir_path,
            pattern=pattern,
            category=category,
            quiet=True,
        )
        for file, errors in results.items():
            if errors:
                domain_key = file.name.split("-")[-1].split(".")[0]
                domain_name = domain_map.get(domain_key, domain_key)
                domain_summary[domain_name][category] += len(errors)

    index_stats = check_index_consistency(
        EXPERTS_DIR, INDEXES_DIR, METADATA_FILE, quiet=True
    )
    for domain, stats in index_stats.items():
        domain_summary[domain]["missing_indexes"] = stats["missing"]
        domain_summary[domain]["orphan_indexes"] = stats["orphans"]

    ethics_stats = check_ethic_consistency(
        EXPERTS_DIR, ETHICS_DIR, METADATA_FILE, quiet=True
    )
    for domain, stats in ethics_stats.items():
        domain_summary[domain]["missing_ethics"] = stats["missing"]
        domain_summary[domain]["orphan_ethics"] = stats["orphans"]

    table = Table(show_lines=True)
    table.add_column(
        "Domain", justify="left", style="bold cyan", header_style="bold green"
    )
    table.add_column(
        "Experts", justify="right", style="bright_white", header_style="bold green"
    )
    table.add_column(
        "Indexes", justify="right", style="bright_white", header_style="bold green"
    )
    table.add_column(
        "Ethics", justify="right", style="bright_white", header_style="bold green"
    )
    table.add_column(
        "Missing Indexes",
        justify="right",
        style="bright_white",
        header_style="bold green",
    )
    table.add_column(
        "Orphan Indexes",
        justify="right",
        style="bright_white",
        header_style="bold green",
    )
    table.add_column(
        "Missing Ethics",
        justify="right",
        style="bright_white",
        header_style="bold green",
    )
    table.add_column(
        "Orphan Ethics",
        justify="right",
        style="bright_white",
        header_style="bold green",
    )

    total = {
        "experts": 0,
        "indexes": 0,
        "ethics": 0,
        "missing_indexes": 0,
        "orphan_indexes": 0,
        "missing_ethics": 0,
        "orphan_ethics": 0,
    }

    for domain in sorted(domain_summary):
        counts = domain_summary[domain]
        for key in total:
            total[key] += counts[key]
        table.add_row(
            domain,
            str(counts["experts"]),
            str(counts["indexes"]),
            str(counts["ethics"]),
            str(counts["missing_indexes"]),
            str(counts["orphan_indexes"]),
            str(counts["missing_ethics"]),
            str(counts["orphan_ethics"]),
        )

    table.add_row(
        "[bold yellow]Total[/bold yellow]",
        *[
            f"[bold magenta]{total[key]}[/bold magenta]"
            for key in [
                "experts",
                "indexes",
                "ethics",
                "missing_indexes",
                "orphan_indexes",
                "missing_ethics",
                "orphan_ethics",
            ]
        ],
    )

    console.print(table)


if __name__ == "__main__":
    app()

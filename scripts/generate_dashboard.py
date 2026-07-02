#!/usr/bin/env python3
"""Generate the LinkML Generator Feature Dashboard from compliance test results.

The compliance test suite is the **source of truth** for whether a generator
supports a feature.  Each test is tagged with a category and display name via
the ``@feature_category`` decorator.  This metadata flows into ``summary.yaml``
and is used here to group and render the dashboard.

No external registry or matrix file is needed — everything comes from test results.

Reads:
  - tests/linkml/test_compliance/output/summary.yaml   (compliance test results)

Writes:
  - docs/generators/dashboard.md                        (Sphinx-compatible dashboard)

Usage:
    # 1. Run compliance tests with output enabled
    uv run pytest tests/linkml/test_compliance/ --with-output

    # 2. Generate dashboard from results
    uv run python scripts/generate_dashboard.py
"""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
SUMMARY_PATH = REPO_ROOT / "tests" / "linkml" / "test_compliance" / "output" / "summary.yaml"
SUMMARY_PARTIAL_PATH = SUMMARY_PATH.with_name("summary_partial.yaml")
OUTPUT_PATH = REPO_ROOT / "docs" / "generators" / "dashboard.md"

# Generator display names (framework id → human-readable name)
GENERATOR_DISPLAY_NAMES = {
    "pydantic": "Pydantic",
    "python_dataclasses": "Python DC",
    "jsonschema": "JSON Schema",
    "java": "Java",
    "shacl": "SHACL",
    "shex": "ShEx",
    "jsonld_context": "JSON-LD Ctx",
    "jsonld": "JSON-LD",
    "sql_ddl_sqlite": "SQLite DDL",
    "sql_ddl_postgres": "Postgres DDL",
    "sqlalchemy_imperative": "SQLAlchemy Imp",
    "sqlalchemy_declarative": "SQLAlchemy Dec",
    "owl": "OWL",
    "pandera_polars_class": "Pandera",
    "dataframe_polars_schema": "Polars Schema",
}

# Map ValidationBehavior values to icons
STATUS_ICONS = {
    "implements": "✅",
    "partial": "⚠️",
    "ignores": "❌",
    "coerces": "⚠️",
    "false_positive": "⚠️",
    "incomplete": "⚠️",
    "not_applicable": "⚪",
    "accepts": "✅",
    "mixed": "⚠️",
    "untested": "❓",
}

# Icons used in legend (deduplicated)
LEGEND_ICONS = [
    ("✅", "Fully supported"),
    ("⚠️", "Partial / incomplete / mixed"),
    ("❌", "Not implemented"),
    ("⚪", "Not applicable"),
    ("❓", "Not yet tested"),
]


def load_summary() -> list[dict]:
    """Load compliance test summary.  Returns list of feature dicts.

    Tries summary.yaml first, falls back to summary_partial.yaml.
    """
    path = SUMMARY_PATH if SUMMARY_PATH.exists() else SUMMARY_PARTIAL_PATH
    if not path.exists():
        print(
            "ERROR: No compliance test output found.\nRun: uv run pytest tests/linkml/test_compliance/ --with-output",
            file=sys.stderr,
        )
        sys.exit(1)

    with open(path) as f:
        data = yaml.safe_load(f)
    return data.get("features", [])


def discover_frameworks(features: list[dict]) -> list[str]:
    """Discover all frameworks from test results, in consistent order."""
    frameworks: set[str] = set()
    for feat in features:
        frameworks.update(feat.get("implementations", {}).keys())

    preferred = [
        "pydantic",
        "python_dataclasses",
        "jsonschema",
        "java",
        "shacl",
        "shex",
        "owl",
        "jsonld_context",
        "jsonld",
        "sql_ddl_sqlite",
        "sql_ddl_postgres",
        "pandera_polars_class",
        "dataframe_polars_schema",
        "sqlalchemy_imperative",
        "sqlalchemy_declarative",
    ]
    ordered = [f for f in preferred if f in frameworks]
    ordered.extend(sorted(frameworks - set(ordered)))
    return ordered


def status_icon(status: str) -> str:
    """Convert a ValidationBehavior string to a display icon."""
    return STATUS_ICONS.get(status, "❓")


def aggregate_status(statuses: list[str]) -> str:
    """Compute an aggregate icon for a list of per-feature statuses."""
    if not statuses:
        return "❓"
    applicable = [s for s in statuses if s != "not_applicable"]
    if not applicable:
        return "⚪"
    if all(s in ("implements", "accepts") for s in applicable):
        return "✅"
    if all(s == "untested" for s in applicable):
        return "❓"
    if all(s in ("ignores", "untested") for s in applicable):
        return "❌"
    return "⚠️"


def slug(name: str) -> str:
    """Generate a URL-safe anchor id from a category name."""
    s = name.lower()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s]+", "-", s)
    return s.strip("-")


def generate_dashboard(features: list[dict]) -> str:
    """Generate the complete dashboard Markdown."""
    frameworks = discover_frameworks(features)
    fw_names = [GENERATOR_DISPLAY_NAMES.get(f, f) for f in frameworks]

    # Group features by category (from @feature_category decorator)
    categories: dict[str, list[dict]] = defaultdict(list)
    for feat in features:
        cat = feat.get("category", "Uncategorized")
        categories[cat].append(feat)

    # Stable category order: sort alphabetically but put "Uncategorized" last
    cat_order = sorted(c for c in categories if c != "Uncategorized")
    if "Uncategorized" in categories:
        cat_order.append("Uncategorized")

    lines: list[str] = []

    # Header
    lines.append("(generator-feature-dashboard)=")
    lines.append("")
    lines.append("# Generator Feature Dashboard")
    lines.append("")
    lines.append(
        "This dashboard shows which LinkML metamodel features each generator supports. "
        "**The compliance test suite "
        "([tests/linkml/test_compliance/](https://github.com/linkml/linkml/tree/main/tests/linkml/test_compliance)) "
        "is the source of truth** — every cell below is derived from actual test results."
    )
    lines.append("")
    lines.append(
        "*Regenerate with: "
        "`uv run pytest tests/linkml/test_compliance/ --with-output && "
        "uv run python scripts/generate_dashboard.py`*"
    )
    lines.append("")

    # Legend
    lines.append("## Legend")
    lines.append("")
    lines.append("| Icon | Meaning |")
    lines.append("|------|---------|")
    for icon, label in LEGEND_ICONS:
        lines.append(f"| {icon} | {label} |")
    lines.append("")

    # Summary table
    lines.append("## Summary by Category")
    lines.append("")
    lines.append(
        "Each cell shows the aggregate result across all tests in that category. Scroll down for per-test details."
    )
    lines.append("")

    header = "| Category |"
    sep = "|----------|"
    for name in fw_names:
        header += f" {name} |"
        sep += " :-: |"
    lines.append(header)
    lines.append(sep)

    for cat_name in cat_order:
        cat_feats = categories[cat_name]
        anchor = slug(cat_name)
        row = f'| <a href="#{anchor}">{cat_name}</a> |'
        for fw in frameworks:
            statuses = [feat.get("implementations", {}).get(fw, "untested") for feat in cat_feats]
            row += f" {aggregate_status(statuses)} |"
        lines.append(row)
    lines.append("")

    # Coverage scores
    lines.append("## Coverage Scores")
    lines.append("")
    lines.append("Percentage of tests where the generator fully implements the feature (excluding not-applicable).")
    lines.append("")

    lines.append("| Generator | Implements | Partial | Ignores | N/A | Total | Score |")
    lines.append("|-----------|:----------:|:-------:|:-------:|:---:|:-----:|:-----:|")

    for fw, name in zip(frameworks, fw_names, strict=True):
        impl = part = ign = na = 0
        for feat in features:
            s = feat.get("implementations", {}).get(fw, "untested")
            if s in ("implements", "accepts"):
                impl += 1
            elif s == "not_applicable":
                na += 1
            elif s in ("ignores", "untested"):
                ign += 1
            else:
                part += 1
        total = impl + part + ign
        pct = (impl / total * 100) if total else 0
        lines.append(f"| {name} | {impl} | {part} | {ign} | {na} | {total} | {pct:.0f}% |")
    lines.append("")

    # Detail tables per category
    lines.append("## Details by Category")
    lines.append("")

    for cat_name in cat_order:
        cat_feats = categories[cat_name]
        lines.append(f"### {cat_name}")
        lines.append("")

        header = "| Test |"
        sep = "|------|"
        for name in fw_names:
            header += f" {name} |"
            sep += " :-: |"
        lines.append(header)
        lines.append(sep)

        for feat in sorted(cat_feats, key=lambda f: f.get("display_name", f["name"])):
            display = feat.get("display_name") or feat["name"]
            row = f"| {display} |"
            for fw in frameworks:
                s = feat.get("implementations", {}).get(fw, "untested")
                row += f" {status_icon(s)} |"
            lines.append(row)
        lines.append("")

    # Footer
    lines.append("---")
    lines.append("")
    lines.append(
        "*This dashboard is auto-generated from compliance test results. "
        "To update: run the compliance tests with `--with-output`, "
        "then run `uv run python scripts/generate_dashboard.py`. "
        "To add features, write a new compliance test and decorate it with "
        '`@feature_category("Category Name", "Display Name")`.*'
    )
    lines.append("")

    return "\n".join(lines)


def main() -> int:
    """Load test results and generate dashboard."""
    features = load_summary()
    content = generate_dashboard(features)
    OUTPUT_PATH.write_text(content)

    # Stats
    cats = defaultdict(int)
    for feat in features:
        cats[feat.get("category", "Uncategorized")] += 1

    print(f"Dashboard written to {OUTPUT_PATH}")
    print(f"  {len(features)} features from compliance tests")
    print(f"  {len(cats)} categories: {', '.join(f'{k} ({v})' for k, v in sorted(cats.items()))}")

    uncategorized = [f["name"] for f in features if f.get("category", "Uncategorized") == "Uncategorized"]
    if uncategorized:
        print(f"  ⚠ {len(uncategorized)} uncategorized (add @feature_category decorator):")
        for name in sorted(uncategorized):
            print(f"    - {name}")

    return 0


if __name__ == "__main__":
    sys.exit(main())

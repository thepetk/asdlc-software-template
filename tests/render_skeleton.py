#!/usr/bin/env python3
import argparse
import shutil
import sys
from pathlib import Path

import jinja2
import yaml

SKELETON = Path("templates/paude-agent/skeleton")

CI_RESOURCES = {
    "requests": {"cpu": "100m", "memory": "128Mi"},
    "limits": {"cpu": "500m", "memory": "256Mi"},
}

# Files rendered as Jinja2 templates (Backstage ${{ }} syntax)
TEMPLATE_SUFFIXES = {".yaml", ".json", ".md", ".sh", ".conf"}


def render(content: "str", values: "dict") -> "str":
    """
    Renders a Backstage skeleton file (${{ }}) as Jinja2.
    """
    content = content.replace("${{", "{{")
    env = jinja2.Environment(undefined=jinja2.StrictUndefined)
    return env.from_string(content).render(values=values)


def patch_resources(rendered: "str") -> "str":
    """
    Replaces resource requests/limits in a StatefulSet with CI-safe values.
    """
    doc = yaml.safe_load(rendered)
    for container in (
        doc.get("spec", {})
        .get("template", {})
        .get("spec", {})
        .get("containers", [])
    ):
        container["resources"] = CI_RESOURCES
    return yaml.dump(doc, default_flow_style=False)


def validate_yaml(rendered: "str", rel: "Path") -> "bool":
    """
    Validates that rendered content is valid YAML. Returns True on success.
    """
    try:
        list(yaml.safe_load_all(rendered))
        return True
    except yaml.YAMLError as exc:
        print(f"  YAML ERROR in {rel}: {exc}", file=sys.stderr)
        return False


def main() -> None:
    parser = argparse.ArgumentParser(description="Render paude-agent skeleton")
    parser.add_argument("--values", required=True, help="Path to values YAML file")
    parser.add_argument("--output", required=True, help="Output directory")
    parser.add_argument("--ci", action="store_true", help="Patch resource requests for CI")
    parser.add_argument(
        "--set",
        metavar="KEY=VALUE",
        action="append",
        default=[],
        dest="overrides",
        help="Override a value from the values file (e.g. --set agentType=cursor). Repeatable.",
    )
    args = parser.parse_args()

    if not SKELETON.exists():
        print(f"ERROR: skeleton not found at {SKELETON}", file=sys.stderr)
        sys.exit(1)

    with open(args.values) as f:
        values = yaml.safe_load(f)

    for override in args.overrides:
        if "=" not in override:
            print(f"ERROR: --set value must be KEY=VALUE, got: {override}", file=sys.stderr)
            sys.exit(1)
        key, val = override.split("=", 1)
        if val.lower() == "true":
            val = True
        elif val.lower() == "false":
            val = False
        values[key] = val

    name = values.get("name")
    if not name:
        print("ERROR: 'name' is required in values file", file=sys.stderr)
        sys.exit(1)

    out = Path(args.output)
    if out.exists():
        shutil.rmtree(out)

    errors = 0
    for src in sorted(SKELETON.rglob("*")):
        if not src.is_file():
            continue

        rel = src.relative_to(SKELETON)
        dst = out / rel
        dst.parent.mkdir(parents=True, exist_ok=True)

        content = src.read_text()

        if src.suffix in TEMPLATE_SUFFIXES:
            try:
                rendered = render(content, values)
            except jinja2.UndefinedError as exc:
                print(f"ERROR rendering {rel}: {exc}", file=sys.stderr)
                errors += 1
                continue

            if args.ci and src.suffix == ".yaml" and "kind: StatefulSet" in rendered:
                rendered = patch_resources(rendered)

            if src.suffix == ".yaml" and not validate_yaml(rendered, rel):
                errors += 1

            dst.write_text(rendered)
        else:
            shutil.copy2(src, dst)

        print(f"  {rel}")

    print(f"\nManifests written to: {out}")
    if errors:
        print(f"\nERROR: {errors} file(s) had rendering or validation errors.", file=sys.stderr)
        sys.exit(1)
    else:
        print("All files rendered and validated successfully.")


if __name__ == "__main__":
    main()

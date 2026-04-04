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


def render(content: "str", values: "dict[str, str]") -> "str":
    """
    renders a Backstage skeleton file (${{ }}) as Jinja2.
    """
    content = content.replace("${{", "{{")
    env = jinja2.Environment(undefined=jinja2.StrictUndefined)
    return env.from_string(content).render(values=values)


def patch_resources(rendered: "str") -> "str":
    """
    replaces resource requests/limits in a Deployment with CI-safe values.
    """
    doc = yaml.safe_load(rendered)
    for container in doc.get("spec", {}).get("template", {}).get("spec", {}).get("containers", []):
        container["resources"] = CI_RESOURCES
    return yaml.dump(doc, default_flow_style=False)


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
        # coerce "true"/"false" strings to booleans to match Jinja2 expectations
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

    for src in sorted(SKELETON.rglob("*.yaml")):
        rel = src.relative_to(SKELETON)

        # rename components/http -> components/<name>
        # this mirrors the fs:rename step functionality
        parts = list(rel.parts)
        if "http" in parts:
            parts[parts.index("http")] = name
        dst = out / Path(*parts)
        dst.parent.mkdir(parents=True, exist_ok=True)

        content = src.read_text()
        try:
            rendered = render(content, values)
        except jinja2.UndefinedError as exc:
            print(f"ERROR rendering {rel}: {exc}", file=sys.stderr)
            sys.exit(1)

        if args.ci and src.name == "deployment.yaml" and "kind: Deployment" in rendered:
            rendered = patch_resources(rendered)

        dst.write_text(rendered)
        print(f"  {rel} -> {Path(*parts)}")

    # overlay path for kubectl apply -k
    overlay = out / "components" / name / "overlays" / "development"
    print(f"\nManifests written to: {out}")
    print(f"Apply with:\n  kubectl apply -k {overlay}")


if __name__ == "__main__":
    main()

# Tests

This directory contains the CI test tooling for validating that the `paude-agent` template skeleton renders correctly and produces valid YAML.

## Files

| File                 | Purpose                                                                            |
| -------------------- | ---------------------------------------------------------------------------------- |
| `render_skeleton.py` | Renders the Jinja2 skeleton into files and validates all YAML files parse cleanly  |
| `ci-values.yaml`     | Values passed to the renderer for CI (simulates `catalog:fetch` outputs and deployment params) |

## Usage

Run from the repo root:

```bash
# Render and validate (inspect the output)
python tests/render_skeleton.py \
  --values tests/ci-values.yaml \
  --output /tmp/ci-manifests

# Render with CI-safe resource patches on the StatefulSet
python tests/render_skeleton.py \
  --values tests/ci-values.yaml \
  --output /tmp/ci-manifests \
  --ci

# Override a single value (e.g. test cursor agent type)
python tests/render_skeleton.py \
  --values tests/ci-values.yaml \
  --set agentType=cursor \
  --set name=ci-cursor \
  --output /tmp/ci-manifests
```

The script exits with a non-zero status if any file fails to render or if any YAML file is syntactically invalid.

## What is validated

- All skeleton files render without Jinja2 `UndefinedError`
- All `.yaml` files in the rendered output parse without `yaml.YAMLError`

The rendered output mirrors the GitOps repository layout that the scaffolder creates at runtime:

```
<output>/
├── build/
│   ├── Dockerfile
│   └── entrypoint*.sh  (stubs)
├── manifests/
│   ├── statefulset.yaml   (replicas: 0)
│   ├── buildconfig.yaml
│   ├── imagestream.yaml
│   ├── pvc.yaml
│   ├── networkpolicy.yaml
│   └── kustomization.yaml
├── argocd/
│   └── application.yaml
├── task/
│   └── TASK.md
├── role/
│   └── CLAUDE.md
├── paude.json
└── catalog-info.yaml
```

## Dependencies

```bash
pip install jinja2 pyyaml
```

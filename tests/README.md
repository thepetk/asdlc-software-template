# Tests

This directory contains the CI test tooling for validating that the `paude-agent` template produces manifests that deploy correctly on Kubernetes.

## Files

| File                 | Purpose                                                                    |
| -------------------- | -------------------------------------------------------------------------- |
| `render_skeleton.py` | Script that renders the Jinja2 skeleton into deployable K8s YAML           |
| `ci-values.yaml`     | Values passed to the renderer for CI (agent name, type, secret name, etc.) |

### Usage

Run from the repo root:

```bash
# Render only (inspect the output)
python tests/render_skeleton.py \
  --values tests/ci-values.yaml \
  --output /tmp/ci-manifests

# Render with CI resource patches
python tests/render_skeleton.py \
  --values tests/ci-values.yaml \
  --output /tmp/ci-manifests \
  --ci
```

The script prints the apply command at the end:

```
Apply with:
  kubectl apply -k /tmp/ci-manifests/components/ci-agent/overlays/development
```

### Dependencies

```bash
pip install jinja2 pyyaml
```

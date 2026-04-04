# Paude Software Template

## What is Paude?

[Paude](https://github.com/bbrowning/paude) runs AI coding agents in secure, isolated containers on `OpenShift`. Because the container network is filtered by a proxy sidecar, agents can be run in autonomous (`--yolo`) mode safely.

## What this template creates

This template creates a single GitOps repository that contains:

- **`catalog-info.yaml`** — Registers the agent as a component of type `agent` in RHDH with enriched `paude.io/*` annotations.
- **`application.yaml`** — The root ArgoCD Application (app-of-apps pattern).
- **`app-of-apps/`** — ArgoCD child Application targeting the deployment overlays.
- **`components/<name>/`** — Kustomize base + development overlay with the Kubernetes Deployment, PVC, and agent ConfigMap.

ArgoCD continuously reconciles the repository, keeping the deployed agent in sync with the GitOps state.

## Supported agents

| Agent                      | Image                                          | Default provider               |
| -------------------------- | ---------------------------------------------- | ------------------------------ |
| **Claude Code** (`claude`) | `quay.io/bbrowning/paude-base-centos10:0.15.0` | Anthropic API / Vertex AI      |
| **Cursor** (`cursor`)      | `quay.io/bbrowning/paude-base-centos10:0.15.0` | Cursor API                     |
| **Gemini CLI** (`gemini`)  | `quay.io/bbrowning/paude-base-centos10:0.15.0` | Google Cloud / Vertex AI       |
| **OpenClaw** (`openclaw`)  | `ghcr.io/openclaw/openclaw:latest`             | OpenAI / Anthropic / Vertex AI |

## Prerequisites

Before running this template you need:

1. **A Kubernetes Secret** in the target namespace containing the credentials for your chosen agent. All keys in the secret are injected as environment variables. Examples:

   | Agent                | Required env var(s)                                   |
   | -------------------- | ----------------------------------------------------- |
   | Claude + Anthropic   | `ANTHROPIC_API_KEY`                                   |
   | Claude + Vertex AI   | `ANTHROPIC_VERTEX_PROJECT_ID`, `GOOGLE_CLOUD_PROJECT` |
   | Cursor               | `CURSOR_API_KEY`                                      |
   | Gemini               | `GOOGLE_CLOUD_PROJECT`                                |
   | OpenClaw + OpenAI    | `OPENAI_API_KEY`                                      |
   | OpenClaw + Anthropic | `ANTHROPIC_API_KEY`                                   |

   ```bash
   oc create secret generic my-agent-secret \
     --from-literal=ANTHROPIC_API_KEY=sk-ant-... \
     -n rhdh-app
   ```

2. **ArgoCD** configured in RHDH with a valid instance and project.

3. **RHDH plugins**: `backstage-plugin-argocd`, `backstage-plugin-kubernetes`, and the dynamic paude plugin for monitoring agents.

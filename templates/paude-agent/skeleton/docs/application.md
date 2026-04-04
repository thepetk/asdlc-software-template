# Paude Agent Application

## Environment variables

The agent container receives environment variables from two sources:

### Always injected

| Variable | Value | Description |
|----------|-------|-------------|
| `PAUDE_WORKSPACE` | `/pvc/workspace` | Path to the agent's code workspace inside the container |
| `PAUDE_AGENT_NAME` | `claude` / `cursor` / `gemini` / `openclaw` | The active agent |
| `PAUDE_SUPPRESS_PROMPTS` | `1` | Suppresses interactive prompts |
| `NODE_USE_ENV_PROXY` | `1` | Enables proxy for Node.js agents (cursor, gemini, openclaw) |

### Injected when autonomous mode is enabled (Claude only)

| Variable | Value |
|----------|-------|
| `PAUDE_AGENT_ARGS` | `--dangerously-skip-permissions` |

### Injected from your credentials Secret

All keys in the secret named in `apiKeySecretName` become env vars automatically via `envFrom.secretRef`.

## Connecting to a running agent

The paude agent runs inside the container and does not expose a terminal by default. To interact with it:

```bash
# Get the pod name
oc get pods -n <namespace> -l paude.io/session-name=<agent-name>

# Open a shell inside the container
oc exec -it <pod-name> -n <namespace> -- bash

# Attach to the agent's tmux session
tmux attach-session -t claude   # or cursor / gemini
```

## OpenClaw web UI

If you deployed an **OpenClaw** agent, it exposes a web UI on port `18789`. The template creates a ClusterIP Service and a TLS-terminated OpenShift Route. Find the route URL with:

```bash
oc get route <agent-name> -n <namespace> -o jsonpath='{.spec.host}'
```

Then open `https://<route-host>` in your browser.

## Autonomous (yolo) mode

When **Enable Autonomous Mode** is checked in the template for a Claude agent, the `--dangerously-skip-permissions` flag is passed. This allows Claude Code to execute actions without asking for confirmation.

> **Warning**: Autonomous mode is safe when network domains are restricted (the default). Avoid setting `allowedDomains: all` in combination with autonomous mode.

## Workspace persistence

The agent's workspace is stored in a `PersistentVolumeClaim` (default: 10Gi). The PVC is **not** deleted when the Deployment is removed — code changes made by the agent persist across restarts. To reset the workspace, delete the PVC manually:

```bash
oc delete pvc <agent-name>-workspace -n <namespace>
```

## Updating the agent image

The TAD gitops annotations on the Deployment allow RHDH to update the container image via the GitOps plugin. The current image path is `.spec.template.spec.containers[0].image`.

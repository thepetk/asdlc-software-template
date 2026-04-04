# paude-software-template

RHDH Software Templates for the [Paude](https://github.com/bbrowning/paude) agentic platform. Register this repo as a catalog location in Red Hat Developer Hub to make all five templates available in the Scaffolder.

## Templates

| Template                  | Catalog type            | Description                                                                                                   |
| ------------------------- | ----------------------- | ------------------------------------------------------------------------------------------------------------- |
| **Paude Agent**           | `agent`                 | Deploy a containerized AI coding agent (Claude, Cursor, Gemini, or OpenClaw) on OpenShift via GitOps (ArgoCD) |
| **Paude Task**            | `agent-task`            | Define a task — a set of goals and context — that can be assigned to an agent                                 |
| **Paude Agent Role**      | `agent-role`            | Define a reusable role/persona that describes an agent's mission and objectives                               |
| **Paude Agent Group**     | `agent-group`           | Group multiple agents under shared objectives for orchestration by the dynamic plugin                         |
| **Paude Task Assignment** | `agent-task-assignment` | Bind a task to a specific agent with a status and optional comment                                            |

## Prerequisites

- Red Hat Developer Hub 1.4+ with the Scaffolder plugin enabled
- GitHub integration configured in RHDH
- ArgoCD instance registered in RHDH (for the `paude-agent` template only)
- A Kubernetes Secret pre-created in the target namespace containing the agent's API credentials (e.g. `ANTHROPIC_API_KEY` for Claude)

## Usage

### Create an Agent

Run the **Paude Agent** template. It will:

1. Create a GitHub repo with Kustomize-based GitOps manifests
2. Register a new `agent` component in the RHDH catalog with `paude.io/*` annotations
3. Create an ArgoCD app-of-apps that syncs the manifests to your OpenShift cluster

Supported agent types and their required secret keys:

| Agent       | Image                                          | Required secret key              |
| ----------- | ---------------------------------------------- | -------------------------------- |
| Claude Code | `quay.io/bbrowning/paude-base-centos10:0.15.0` | `ANTHROPIC_API_KEY`              |
| Cursor      | `quay.io/bbrowning/paude-base-centos10:0.15.0` | `CURSOR_API_KEY`                 |
| Gemini CLI  | `quay.io/bbrowning/paude-base-centos10:0.15.0` | `GEMINI_API_KEY`                 |
| OpenClaw    | `ghcr.io/openclaw/openclaw:latest`             | `OPENAI_API_KEY` (or equivalent) |

### Define tasks and roles (optional)

Use the remaining templates to build out the agentic model in the catalog:

- **Paude Task** — create tasks with goals and context
- **Paude Agent Role** — create reusable roles (e.g. "DevOps Expert") with objectives
- **Paude Agent Group** — group agents for multi-agent orchestration
- **Paude Task Assignment** — assign a task to an agent and track its status (`todo` → `in-progress` → `done`)

The `paude.io/*` annotations on all catalog entities are consumed by the Paude dynamic plugin to monitor and orchestrate agents from within RHDH.

## Contributing

Feel free to create a PR with your suggested changes for this repo.

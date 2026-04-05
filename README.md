# Agentic SDLC Software Templates

Agentic Software Development Lifecycle Software Templates based on [Paude](https://github.com/bbrowning/paude). Register this repo as a catalog location in Red Hat Developer Hub to make all templates available in the Scaffolder.

## Templates

| Template                     | Catalog type       | Description                                                                                                              |
| ---------------------------- | ------------------ | ------------------------------------------------------------------------------------------------------------------------ |
| **Paude Project Repository** | `paude-project`    | Create the shared GitHub repository that all agents in a workflow write to. Adds a Tekton pipeline for agent sequencing. |
| **Paude Task**               | `paude-task`       | Define a task — title, description, objectives, and acceptance criteria — that drives an agent's TASK.md.                |
| **Paude Agent Role**         | `paude-agent-role` | Define a reusable agent persona: a system prompt and agent type (Claude, Gemini, or Cursor).                             |
| **Paude Agent**              | `paude-agent`      | Deploy a paude agent session on OpenShift. Binds a Role, a Task, and a Paude Project Repository together.                |

## Prerequisites

- Red Hat Developer Hub 1.4+ with the Scaffolder plugin enabled
- GitHub integration configured in RHDH
- ArgoCD instance registered in RHDH (`argocd:create-resources` action must be available — RHDH built-in)
- Tekton Pipelines installed and integrated in the RHDH instance
- An OpenShift cluster where agents will run

## Usage

### Typical workflow

The templates are designed to be used in this order:

#### 1. Create a Paude Project Repository

Run the **Paude Project Repository** template. It will:

1. Create a GitHub repo with a Tekton `EventListener` and `Pipeline` under `.tekton/`
2. Create an empty `pipeline-config.yaml` (populated automatically as agents are created)
3. Register the project as a `paude-project` component in the RHDH catalog
4. Create an ArgoCD application that keeps the Tekton resources in sync via GitOps

#### 2. Create Roles and Tasks

Use these templates to define the building blocks for agents:

- **Paude Agent Role** — define a persona with a full system prompt and agent type (`claude`, `gemini`, or `cursor`)
- **Paude Task** — define a unit of work with objectives and acceptance criteria

#### 3. Create Paude Agents

Run the **Paude Agent** template for each agent in the workflow. It will:

1. Resolve the selected Role, Task, and Project Repository from the catalog
2. Create a GitOps repository containing:
   - `build/Dockerfile` — installs the agent onto the base image
   - `manifests/` — StatefulSet (`replicas: 0`), BuildConfig, ImageStream, PVC, NetworkPolicy
   - `role/CLAUDE.md` — system prompt from the Role entity
   - `task/TASK.md` — task description, objectives, and acceptance criteria from the Task entity
   - `paude.json` — network domain allowlist and extra packages
3. Register the agent as a `paude-agent` component in the catalog (with `dependsOn` links to its Role, Task, and Project)
4. Create an ArgoCD application pointing at `manifests/` — ArgoCD provisions the session automatically
5. Open a PR on the Paude Project repo to append the agent to `pipeline-config.yaml`

ArgoCD syncs the manifests, triggering an image build. The session starts (`replicas: 1`) when the user runs `paude start <name>` or when the Tekton pipeline triggers it.

### Supported agent types

Agent type is set on the **Role** entity, not on the agent directly.

| Agent Type  | Value    | Base Image                                     |
| ----------- | -------- | ---------------------------------------------- |
| Claude Code | `claude` | `quay.io/bbrowning/paude-base-centos10:0.15.0` |
| Cursor      | `cursor` | `quay.io/bbrowning/paude-base-centos10:0.15.0` |
| Gemini CLI  | `gemini` | `quay.io/bbrowning/paude-base-centos10:0.15.0` |

### Multi-agent workflows

Each `paude-agent` declares a `trigger` and optionally a `triggeredBy` agent. The Tekton pipeline in the Paude Project repo reads `pipeline-config.yaml` on every push or PR event and starts the next agent automatically.

| `trigger` value | When it fires                                                |
| --------------- | ------------------------------------------------------------ |
| `manual`        | Never — user starts the agent explicitly with `paude start`  |
| `pr-opened`     | When the `triggeredBy` agent opens a pull request            |
| `ci-passed`     | When CI passes on the `triggeredBy` agent's PR (recommended) |
| `pr-merged`     | When the `triggeredBy` agent's PR is merged                  |

## Contributing

Feel free to create a PR with your suggested changes for this repo.

# Agentic SDLC Software Templates

Agentic Software Development Lifecycle Software Templates based on [Paude](https://github.com/bbrowning/paude). Register this repo as a catalog location in Red Hat Developer Hub to make all templates available in the Scaffolder.

## Templates

| Template                     | Catalog type       | Description                                                                                                                         |
| ---------------------------- | ------------------ | ----------------------------------------------------------------------------------------------------------------------------------- |
| **Paude Project Repository** | `paude-project`    | Create the shared GitHub repository that all agents in a workflow write to. Adds a Pipelines as Code pipeline for agent sequencing. |
| **Paude Task**               | `paude-task`       | Define a task — title, description, objectives, and acceptance criteria — that drives an agent's TASK.md.                           |
| **Paude Agent Role**         | `paude-agent-role` | Define a reusable agent persona: a system prompt and agent type (Claude, Gemini, or Cursor).                                        |
| **Paude Agent**              | `paude-agent`      | Deploy a paude agent session on OpenShift. Binds a Role, a Task, and a Paude Project Repository together.                           |

## Prerequisites

- Red Hat Developer Hub 1.4+ with the Scaffolder plugin enabled
- GitHub integration configured in RHDH
- ArgoCD instance registered in RHDH (`argocd:create-resources` action must be available — RHDH built-in)
- **OpenShift Pipelines with Pipelines as Code (PaC) enabled** on the cluster
- A GitHub App (or token) configured in PaC
- An OpenShift cluster where agents will run

## Secrets

Before scaffolding a Paude Project Repository, a cluster admin must create a Kubernetes Secret in the target ArgoCD namespace. This secret provides the GitHub token and webhook secret that Pipelines as Code uses to validate and respond to webhook events.

### Required secret

**Name:** `pipelines-as-code-secret`
**Namespace:** the ArgoCD namespace you enter in the template (`argoNS`, e.g. `openshift-gitops`)

| Key              | Description                                                                                           |
| ---------------- | ----------------------------------------------------------------------------------------------------- |
| `provider.token` | GitHub Personal Access Token (or GitHub App installation token) with `repo` and `checks:write` scopes |
| `webhook.secret` | Random string set as the **Webhook secret** when configuring the GitHub App or repository webhook     |

**Create the secret:**

```bash
oc create secret generic pipelines-as-code-secret \
  -n <argoNS> \
  --from-literal=provider.token=<github-token> \
  --from-literal=webhook.secret=<webhook-secret>
```

For detailed cluster-admin instructions (GitHub App setup, multi-namespace configuration), see [docs/cluster-admin-setup.md](docs/cluster-admin-setup.md).

## Usage

### Typical workflow

The templates are designed to be used in this order:

#### Create a Paude Project Repository

Run the **Paude Project Repository** template. It will:

1. Create a GitHub repo with a Pipelines as Code `Repository` CRD and annotated `PipelineRun` under `.tekton/`
2. Create an empty `pipeline-config.yaml` (populated automatically as agents are created)
3. Register the project as a `paude-project` component in the RHDH catalog
4. Create an ArgoCD application that keeps the `.tekton/` resources in sync via GitOps

#### Create Roles and Tasks

Use these templates to define the building blocks for agents:

- **Paude Agent Role** — define a persona with a full system prompt and agent type (`claude`, `gemini`, or `cursor`)
- **Paude Task** — define a unit of work with objectives and acceptance criteria

Both templates open a pull request that adds a `catalog-info.yaml` under `examples/<name>/` in the catalog repository you specify. Once the PR is merged, the entity is automatically discovered and available in RHDH - no separate GitHub repository is created.

> **Tip:** The `examples/` directory in this repo contains ready-to-use roles and tasks you can import directly instead of running the templates from scratch. See [examples/](#examples) below.

#### Create Paude Agents

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

ArgoCD syncs the manifests, triggering an image build. The session starts (`replicas: 1`) when the user runs `paude start <name>` or when the Pipelines as Code pipeline triggers it.

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

## Examples

Ready-to-use roles and tasks live under `examples/`. They are registered automatically via the `./examples/*/catalog-info.yaml` glob in the root `catalog-info.yaml`.

| Example                                                                       | Type               | Description                                                                 |
| ----------------------------------------------------------------------------- | ------------------ | --------------------------------------------------------------------------- |
| [`software-engineer-role`](examples/software-engineer-role/catalog-info.yaml) | `paude-agent-role` | Claude Code agent that writes code, tests, and opens PRs                    |
| [`flask-app-task`](examples/flask-app-task/catalog-info.yaml)                 | `paude-task`       | Build a minimal Python Flask app with a `/health` endpoint and pytest tests |

To add your own, either run the **Paude Agent Role** / **Paude Task** template (opens a PR automatically) or manually create `examples/<name>/catalog-info.yaml` and open a PR to this repo.

## Contributing

Feel free to create a PR with your suggested changes for this repo.

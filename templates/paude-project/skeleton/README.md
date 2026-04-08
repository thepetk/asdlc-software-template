# ${{ values.name }}

${{ values.description }}

## Work Branch

All Paude agents in this project push commits to: `${{ values.workBranch }}`

## Pipelines as Code

The `.tekton/` directory contains two files that wire this repository into the cluster's Pipelines as Code (PaC) installation:

- **`repository.yaml`** — a `Repository` CRD that registers this repo with PaC. PaC uses it to validate incoming webhooks and clone the repo.
- **`pipelinerun.yaml`** — a PaC-annotated `PipelineRun` template. PaC creates a new run from this file on every matching push, pull request, or check suite event, automatically injecting event variables (revision, branch, PR number, etc.).

On every qualifying event, the pipeline:

1. Clones this repository at the event revision.
2. Reads `pipeline-config.yaml` to find the next agent to trigger.
3. Patches the agent's StatefulSet with dynamic runtime context (PR number, branch, etc.).
4. Scales the agent's StatefulSet to `replicas: 1` to start it.
5. Logs a notification with the event details.

## Agent Pipeline Config

`pipeline-config.yaml` lists all agents and their trigger rules. Each `paude-agent` template
run appends one entry to this file automatically.

## Prerequisites

- OpenShift Pipelines with **Pipelines as Code** enabled on the cluster.
- A Kubernetes Secret named **`pipelines-as-code-secret`** must exist in namespace **`${{ values.argoNS }}`** before ArgoCD syncs `.tekton/` for the first time. See [cluster admin setup](https://github.com/${{ values.repoOwner }}/${{ values.name }}) or ask your cluster admin to follow `docs/cluster-admin-setup.md` in the template repository.
- The `argocd:create-resources` scaffolder action must be available (RHDH built-in).

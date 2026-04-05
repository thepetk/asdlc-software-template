# ${{ values.name }}

${{ values.description }}

## Work Branch

All Paude agents in this project push commits to: `${{ values.workBranch }}`

## Tekton Pipeline

The `.tekton/` directory contains a Tekton `Pipeline` and `EventListener` that orchestrate
the multi-agent workflow. On every push or pull request event, the pipeline:

1. Reads `pipeline-config.yaml` to find the next agent to trigger.
2. Patches the agent's StatefulSet with dynamic runtime context (PR number, branch, etc.).
3. Scales the agent's StatefulSet to `replicas: 1` to start it.
4. Posts a webhook notification with the event details.

## Agent Pipeline Config

`pipeline-config.yaml` lists all agents and their trigger rules. Each `paude-agent` template
run appends one entry to this file automatically.

## Prerequisites

- RHDH instance with ArgoCD and Tekton Pipelines installed and integrated.
- The `argocd:create-resources` scaffolder action must be available (RHDH built-in).

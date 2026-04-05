# Task: ${{ values.taskTitle }}

## Description

${{ values.taskDescription }}

## Objectives

{%- for obj in values.taskObjectives %}
- {{ obj }}
{%- endfor %}

## Acceptance Criteria

{%- for ac in values.taskAcceptanceCriteria %}
- {{ ac }}
{%- endfor %}

## Branch

Work on branch: `${{ values.workBranch }}`
Push to: `${{ values.projectRepoUrl }}`

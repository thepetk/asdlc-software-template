# ${{ values.name }}

${{ values.description }}

## Objectives

{%- for objective in values.objectives %}
- {{ objective }}
{%- endfor %}

## Acceptance Criteria

{%- for criterion in values.acceptanceCriteria %}
- {{ criterion }}
{%- endfor %}

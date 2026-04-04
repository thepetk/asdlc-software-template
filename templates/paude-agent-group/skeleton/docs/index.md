# ${{ values.title }}

${{ values.description }}

## Objectives

{% for objective in values.objectives %}
- {{ objective }}
{% endfor %}

## Member Agents

{% for agent in values.agents %}
- {{ agent }}
{% endfor %}

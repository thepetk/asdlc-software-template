# ${{ values.title }}

${{ values.description }}

## Objectives

{% for objective in values.objectives %}
- {{ objective }}
{% endfor %}

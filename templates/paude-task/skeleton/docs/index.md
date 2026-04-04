# ${{ values.name }}

${{ values.description }}

## Goals

{% for goal in values.goals %}
- {{ goal }}
{% endfor %}

{% if values.additionalContext %}
## Additional Context

{% for line in values.additionalContext %}
- {{ line }}
{% endfor %}
{% endif %}

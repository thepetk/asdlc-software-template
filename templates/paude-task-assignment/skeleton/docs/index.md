# ${{ values.name }}

Assignment of **${{ values.task }}** to **${{ values.agent }}**.

## Details

| Field   | Value               |
|---------|---------------------|
| Agent   | ${{ values.agent }} |
| Task    | ${{ values.task }}  |
| Status  | ${{ values.status }}|

{% if values.comment %}
## Comment

${{ values.comment }}
{% endif %}

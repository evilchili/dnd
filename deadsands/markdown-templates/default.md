---
# {{filename}}

title: {{ title }}
author: {{ author if author else 'evilchili' }}
show_dm_content: False
tags: {{ tags }}
{% if date %}
date: {{ date }}
{% endif %}
{% if summary %}
  summary: {{summary}}
{% endif %}
status: {{ status if status else 'publish }}
---


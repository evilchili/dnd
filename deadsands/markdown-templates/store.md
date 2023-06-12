---
# {{filename}}

title: {{ title }}
author: {{ author if author else 'evilchili' }}
show_dm_content: False
tags: {{ tags }}
{% if date %}
date: {{ date }}
{% endif %}
{% if description %}
description: {{description}}
{% endif %}
status: {{ status if status else 'published' }}
---

{{ summary }}


Location: **{{location}}**

Faction: **{{faction}}**


### Current Stock

{{ inventory }} 

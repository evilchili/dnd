---
# {{filename}}

title: {{ title }}
author: {{ author if author else 'evilchili' }}
tags: {{ tags or 'location'}}
{% if date %}
date: {{ date }}
{% endif %}
template: location
show_dm_content: False
thumbnail: /images/{{ title|slugify }}_thumb.png
image: /images/{{title|slugify}}.png
{% if summary %}
  summary: {{summary}}
{% endif %}
location:
  type: settlment
  name: {{ title }}
  population: 1000
  notable_races: humans
  economy: textiles
  dm_notes: |
    DM's notes go here.
  stores:
status: {{ status if status else 'draft' }}
---

{{ description }}

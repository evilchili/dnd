---
# {{filename}}

title: {{ title }}
author: {{ author if author else 'evilchili' }}
tags: {{ tags or 'region'}}
{% if date %}
date: {{ date }}
{% endif %}
template: region
{% if summary %}
  summary: {{summary}}
{% endif %}
region:
  name: {{ title }}
  size: 10
  terrain: difficult
  description: |
    description
  skills:
    travel:
        dc: 10
        notes:
    forage:
        dc: 10
        notes:
    track:
        dc: 10
        notes:
    evade:
        dc: 10
        notes:
    survey:
        dc: 10
        notes:
  cr: 4
  encounters:
{% rolltable ['encounters'], indent=4 %}
  weather:
{% rolltable ['weather'], indent=4 %}
  regional_effects:
    -
    -
status: {{ status if status else 'draft' }}
---

DM's region notes goes here.

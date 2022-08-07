---
# {{filename}}

title: {{ title }}
author: {{ author if author else 'evilchili' }}
tags: {{ tags or 'region'}}
{% if date %}
date: {{ date }}
{% endif %}
template: region
show_dm_content: False
{% if summary %}
  summary: {{summary}}
{% endif %}
region:
  name: {{ title }}
  size: 10
  terrain: difficult
  dm_notes: |
    DM's notes go here.
  skills:
    Travel:
        DC: 10
        Notes:
    Forage:
        DC: 10
        Notes:
    Track:
        DC: 10
        Notes:
    Evade:
        DC: 10
        Notes:
    Survey:
        DC: 10
        Notes:
  cr: 4
  encounters:
{% rolltable ['encounters'], die=20, indent=4 %}
  weather:
{% rolltable ['weather'], indent=4 %}
  regional_effects:
{% rolltable ['regional_effects'], die=1, indent=4 %}
status: {{ status if status else 'draft' }}
---

Description goes here.

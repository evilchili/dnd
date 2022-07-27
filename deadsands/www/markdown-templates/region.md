---
# {{filename}}

title: {{ title }}
author: {{ author if author else 'evilchili' }}
tags: {{ tags }}
{% if date %}
date: {{ date }}
{% endif %}
category: regions
template: region
{% if summary %}
  summary: {{summary}}
{% endif %}
region:
    name: {{ title }}
    size: 10
    terrain: difficult
    shelter: none
    water_source: none
    travel:
        dc: 10
        critical_success: 
        critical_fail: 
    forage:
        dc: 10
        critical_success: 
        critical_fail: 
    track:
        dc: 10
        critical_success: 
        critical_fail: 
    evade:
        dc: 10
        critical_success: 
        critical_fail: 
    survey:
        dc: 10
        critical_success: 
        critical_fail: 
    encounter_chance: 5
    special:
    weather:
        d1:
        d2:
        d3:
        d4:
        d5:
        d6:
        d7:
        d8:
status: {{ status if status else 'draft' }}
---

Region description goes here.

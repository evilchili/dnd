---
# /Users/evilchili/dnd/deadsands/www/content/region/blooming-wastes.md

title: The Blooming Wastes
author: evilchili
tags: region, homebrew
date: 2022-07-20 17:54:47.286869
description: Once you have surveyed a region you will gain access a subset of this information; others, like weather and regional effects, must be discovered.
template: region
region:
    name: The Blooming Wastes
    size: 20
    terrain: difficult
    description:  |
        The Blooming Wastes stretch out before you: a mostly flat expanse of hard,  cracked earth blanketed by some kind of sandy brown scrub. Small mesas dot the horizon, suggesting the possibility of shelter. As you approach you see that the scrub is covered in thick black thorns sharp enough to pierce boot leather; you will need to tread carefully. 
    travel:
        dc: 10
        critical_success: normal terrain
        critical_failure: 
        resources:
    forage:
        dc: 10
        critical_success: 
        critical_failure: 
        resources: redfoot, moon blossom (night only)
    track:
        dc: 13
        critical_success: 
        critical_failure: shelter occupied; random encounter
        resources: shelter, water
    evade:
        dc: 2
        critical_success: 
        critical_failure: random encounter
    survey:
        dc: 13
        critical_success: 
        critical_failure: 
    encounters: 1-6
    cr: 4
    regional_effects:
        - Add 1d6 to radiant damage 
        - Nightvision not functional
        - When a spell attack misses, it hits a random creature within 5 feet instead
        - On a spell attack critical hit or miss, roll on the Wild Magic Table
        - 1d4 piercing damage for every 30ft of movement during the Dash action
    weather:
        d1: Scorching Temperatures - 2x water consumption
        d2: Hail (no effect - counts as magical water if consumed)
        d3: Ghostly Wailing - Disadvantage on concentration checks
        d4: Low Oxygen - Disadvantage on STR Athletics checks and saves 
        d5: Extra Gravity - Disadvantage on DEX checks and saves
        d6: Hot Metal Storm - Heat Metal spell effects for half-day
        d7: Bubble Rain - Bubbles rain upwards, obscuring vision; disadvantage on perception checks
        d8: Clear Skies (No effect)
---

A mostly flat expanse of hard-packed earth blanked by redfoot, a hardy, sandy-brown moss covered in sharp thorns. At night glowing clusters of moon blossoms emerge from the earth and open their petals, bathing the entire wasteland in a pale, silvery light.

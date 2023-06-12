---
# regions/the-haunted-hills.md

title: The Haunted Hills
author: evilchili
tags: region
date: 2023-06-09 18:36:37.735366
template: region
show_dm_content: False
region:
  name: The Haunted Hills
  size: 20
  terrain: normal
  dm_notes: Talisman of Blightward required to avoid effects of weather.
  skills:
    Travel:
        DC: 19
        Notes: 
    Forage:
        DC: 12
        Notes:
    Track:
        DC: 10
        Notes:
    Evade:
        DC: 13
        Notes:
    Survey:
        DC: 10
        Notes:
  cr: 5
  encounters:
    d1:
      Difficulty: Dangerous
    d2-d3:
      Difficulty: Deadly
    d4-d6:
      Difficulty: Difficult
    d7-d14:
      Difficulty: Easy
    d15-d20:
      Difficulty: None
  weather:
    d1-d2:
      Rarity: Common
      Description: Clear Skies
      Effect: No effect
    d3:
      Rarity: Rare
      Description: Howling Fantods
      Effect: A phantasm appears and disappears at random. Anyone who can see it is frightened.
    d4-d5:
      Description: Ghostly Wailing
      Effect: Disadvantage on CON checks for concentration checks
      Rarity: Uncommon
    d6-d7:
      Rarity: Rare
      Description: Breath of the Dead
      Effect: 1d6 Necrotic damage per half-day
    d8:
      Rarity: Rare
      Description: Soul Blight
      Effect: Maximum HP is reduced by 1d4 per half-day unless wearing a Talisman of Blightward.
  regional_effects:
      - On a spell attack critical hit or miss, roll on the Wild Magic Table
  forage_table:
    d1-d2:
      Rarity: Rare
      Name: Deadbreath
      Description: A tough black root that grows in cracks in the stone. When disturbed, the bark releases Breath of the Dead spores. DC 13 Nature, Survival, Constitution check or 1d4 Necrotic damage.
      Value: 5 GP
    d3:
      Rarity: Uncommon
      Name: Brightshrooms
      Description: |
        A grey, partially translucent mushroom that glows green in the presence of leaving creatures.
      Value: 1 GP
    d4:
      Rarity: Common
      Name: Water
      Description: Cool, crisp, clear. Small pools and springs dot the caverns.
      Value: 1 GP
status: draft
---

South of Gopher Gulch at the base of the eastern range of Hoard's Vault, lies a long series of rocky foothills carved through by howling winds; the interior of the hills is a vast network of tunnels that wail like the moaning of the dead, leading to the popular superstition that the land is cursed.

# Example output

Illustrative output for a small suburban back garden in **Ghent, Belgium** (photo taken
in June): a lawn, a clipped hedge, mixed border shrubs, a cherry tree, and a paved path.
Trimmed for brevity — a real plan lists more tasks. This shows the expected *shape*.

---

## Identified plants

- **Lawn / turf grass** (high) — open mown lawn, some wear/shade patches.
- **Clipped hedge** (medium) — formal green hedge; in this region most likely hornbeam
  (*Carpinus betulus*) or beech (*Fagus sylvatica*).
- **Border shrubs** (medium) — flowering deciduous shrubs in the beds (e.g. *Deutzia* /
  *Weigela* type).
- **Cherry tree** (low) — mature tree at the rear, likely an ornamental/fruiting *Prunus*.

## Climate context

Hardiness zone ~8b. Last spring frost ~mid-April; first autumn frost ~early November.
Wet, mild winters; occasional summer dry spells.

## Month-by-month plan

Every month is listed, in order — quiet months included.

**January** — Dormant. Check tree ties/stakes after winter storms; otherwise nothing required.
**February** — Avoid winter-pruning the cherry (*Prunus* is pruned in summer to limit silver
leaf); instead inspect and tidy the beds.
**March** — Cut back any remaining dead growth; first lawn feed when growth starts.
**April** — Fertilize the lawn; begin regular mowing.
**May** — Continue mowing; start weeding the paths as growth picks up.
**June** — First hedge trim; deadhead spent shrub flowers after flowering.
**July** — Summer-prune the cherry tree.
**August** — Keep mowing and weeding; little structural work needed.
**September** — Second hedge trim; divide overgrown perennials.
**October** — Last mow of the season; begin clearing fallen leaves.
**November** — Rake remaining leaves off the lawn; mulch the beds.
**December** — Dormant. Nothing required beyond clearing heavy leaf litter.

---

```json
{
  "location": {
    "input": "Ghent, Belgium",
    "city": "Ghent",
    "country": "Belgium",
    "hardiness_zone": "8b",
    "frost_window": {
      "last_spring_frost": "mid-April",
      "first_autumn_frost": "early November"
    }
  },
  "plants": [
    { "id": "p1", "common_name": "Lawn / turf grass", "scientific_name": "", "type": "lawn", "confidence": "high", "notes": "Open mown lawn with some shaded/worn patches." },
    { "id": "p2", "common_name": "Clipped hedge", "scientific_name": "Carpinus betulus", "type": "hedge", "confidence": "medium", "notes": "Formal green hedge; hornbeam most likely for the region." },
    { "id": "p3", "common_name": "Border shrub", "scientific_name": "", "type": "shrub", "confidence": "medium", "notes": "Flowering deciduous shrub in the beds." },
    { "id": "p4", "common_name": "Cherry tree", "scientific_name": "Prunus", "type": "tree", "confidence": "low", "notes": "Mature tree at the rear of the garden." }
  ],
  "tasks": [
    { "id": "t1", "title": "First lawn feed", "plant_id": "p1", "category": "fertilizing", "month": "March", "recurrence": "yearly", "instructions": "Apply a spring high-nitrogen lawn feed once growth restarts.", "priority": "medium" },
    { "id": "t2", "title": "Mow the lawn", "plant_id": "p1", "category": "mowing", "month": "April", "recurrence": "monthly", "instructions": "Mow regularly through the growing season (April–October), lowering the cut gradually.", "priority": "medium" },
    { "id": "t3", "title": "Trim the hedge", "plant_id": "p2", "category": "pruning", "month": "June", "recurrence": "seasonal", "instructions": "Trim the hedge in June and again in September to keep a crisp shape.", "priority": "medium" },
    { "id": "t4", "title": "Summer-prune the cherry", "plant_id": "p4", "category": "pruning", "month": "July", "recurrence": "yearly", "instructions": "Prune Prunus in summer, not winter, to reduce silver leaf and bacterial canker risk.", "priority": "high" },
    { "id": "t5", "title": "Divide perennials", "plant_id": "p3", "category": "dividing", "month": "September", "recurrence": "yearly", "instructions": "Lift and split congested clumps to keep them vigorous.", "priority": "low" },
    { "id": "t6", "title": "Rake leaves off the lawn", "plant_id": "p1", "category": "cleanup", "month": "November", "recurrence": "yearly", "instructions": "Clear fallen leaves so the grass isn't smothered over winter.", "priority": "medium" },
    { "id": "t7", "title": "Weed the paths", "plant_id": null, "category": "cleanup", "month": "May", "recurrence": "seasonal", "instructions": "Remove weeds from between the paving slabs as needed through summer.", "priority": "low" }
  ]
}
```

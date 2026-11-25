# NetHack 3.6.7 — Quick Reference Summary

> Condensed from the official Guidebook. For full detail see GUIDEBOOK.md.

---

## The Goal

Descend the Mazes of Menace, retrieve the **Amulet of Yendor** from deep below (beyond ~level 20), and escape alive. You win by ascending back out with the Amulet.

---

## The Screen at a Glance

```
Top line:   messages — press SPACE at "--More--", ^P to replay
Map:        ASCII dungeon (@=you, d/f/u=pet, I=unseen monster)
Bottom:     Dlvl $ HP Pw AC Xp T <hunger>
```

**AC:** lower is better (10=naked, 0=well-armored, negative=great).
**HP 0 = dead. Dead is permanent.**

---

## Essential Keys

```
MOVE        hjkl + yubn (vi keys)   .=wait   _=travel to tile
INVENTORY   i  list   d  drop   ,  pick up   @  autopickup toggle
ITEMS       w  wield   W  wear   T  take off   P  put on ring/amulet
            q  drink   r  read   z  zap   e  eat   a  apply tool
            t  throw   f  fire   Q  set quiver   x  exchange weapons
WORLD       s  search   o  open   c  close   ^D  kick
            >  descend   <  ascend
INFO        :  floor   ;  free-look   /  what glyph?   ^P  messages
META        S  save+quit   ^X  stats   O  options   ?  help
EXTENDED    #pray  #offer  #chat  #enhance  #conduct  #loot  #force
```

---

## BUC Status (Most Important Hidden Attribute)

Every item is **Blessed / Uncursed / Cursed**.

| Status | Key effect |
|--------|-----------|
| Blessed | Better performance (more damage, longer duration) |
| Uncursed | Normal |
| Cursed | Weapon welds to hand; armor won't come off; penalties |

**How to check:** drop items on an altar and step off.
**How to fix:** scroll of remove curse, holy water, or `#pray` in crisis.
Priests sense BUC innately.

---

## Item Types

| Symbol | Type | Command | Note |
|--------|------|---------|------|
| `)` | Weapon | `w` wield | Also throwable with `t` |
| `[` | Armor | `W`/`T` wear/off | Stack: helm+body+cloak+boots+gloves+shield |
| `=` | Ring | `P`/`R` on/off | 2 max; accelerates hunger |
| `"` | Amulet | `P`/`R` on/off | 1 max |
| `!` | Potion | `q` drink | Or `t` throw at monsters |
| `?` | Scroll | `r` read | Scroll of identify = most valuable |
| `/` | Wand | `z` zap | Limited charges; breaking = last resort |
| `+` | Spellbook | `r` study | `Z` to cast |
| `%` | Food | `e` eat | |
| `(` | Tool | `a` apply | Containers: `#loot` |
| `*` | Gem | — | Sell for gold; test on touchstone with `#rub` |
| `$` | Gold | (auto) | Shops, score |

---

## Fighting

- **Melee:** walk into the monster
- **Must be wielded:** `w <letter>` — bare hands deal 1–2 damage (Monk excepted)
- **Throw/shoot:** `t` (any item) or `f` (quiver) — Rangers can fire multiple per turn
- **Flee:** walk away — monster gets one free hit; stairs break line of sight
- **Invisible enemies:** attack by moving into their `I` marker
- **Skill:** use `#enhance` to spend accumulated skill points

---

## Eating

**Hunger ladder:**
```
Satiated → (none) → Hungry → Weak → Fainting → Fainted → Starved (dead)
```

Eat before `Hungry`. `Weak` costs Strength. Satiated in combat can cause choking.

**Safe corpses (fresh only):** newts, rats, kobolds, geckos, gnomes, jackals, lichens
**Avoid:** pets, humans, kobold shamans, bats (causes stun), anything >50 turns old

**If sick:** "You feel feverish" or "deathly sick" → `#pray` immediately. Illness kills in 8–25 turns.

---

## Dungeon Navigation

- **Rooms:** lit rooms are fully visible; dark rooms require adjacency
- **Secret doors:** `s` to search — press multiple times at suspicious walls
- **Traps:** invisible until triggered or found with `s`. Use `#untrap` on containers
- **Stairs:** `>` down · `<` up. Level is saved to disk when you leave
- **Pets:** follow if adjacent when you use stairs; get stranded if not
- **Travel:** `_` for point-to-point autotravel on known map

---

## Shops

- Walk over an item to autopickup-buy; press `p` to pay
- `#chat` on an item to ask price before buying
- Turn off autopickup (`@`) before entering shops
- First tile inside the door counts as outside — crossing while carrying unpaid items triggers payment
- Selling: drop items; shopkeeper may buy or decline
- Shopkeepers run out of money → store credit (shop-specific, non-transferable)

---

## Praying (`#pray`)

Use only in genuine crisis: low HP, starving, sick, badly cursed. Effective roughly once per 800–1000 turns. Spamming angers your god. One prayer per crisis = the rule.

---

## Pets

- Start as small dog `d`, kitten `f`, or pony `u`
- Fight with you, gain experience, feed themselves on corpses (horses need vegetables)
- **Item test:** drop item near pet — if it steps on it, item is not cursed
- Don't throw weapons through them; don't let them eat things you've poisoned

---

## Bones Levels

If you enter a level where a past run died, their ghost `W` is there. Ghost = weak, but their items are usually cursed. The monster that killed them may still lurk.

---

## Conduct (Optional Challenges)

`#conduct` shows which you've maintained. Notable ones:

| Conduct | Rule |
|---------|------|
| Atheist | No praying, sacrificing, or chatting with priests |
| Pacifist | Kill no experience-granting monsters |
| Weaponless | No wielded weapons |
| Vegetarian | No meat |
| Wishless | No wand-of-wishing or other wishes |

---

## Scoring Factors

- Gold accumulated · dungeon depth · experience level reached
- Valuable gems carried out · win bonus for ascending with Amulet
- Conduct bonuses · penalties for dying or quitting

---

## Explore Mode

`#exploremode` (M-x) — relaxes permadeath. You can keep the save file on restore to replay sections. Not the "real" game, but useful for learning.

---

## Top Survival Rules

1. **Check BUC before wearing anything** — altars, priests, or scrolls of identify
2. **Save scrolls of identify** for rings and wands first
3. **`#pray` once per crisis**, not as a heal button
4. **Eat before `Hungry`**, not after
5. **Search suspicious dead ends** (`s` × 5–10)
6. **Don't drink unknown potions near stairs** — teleportation kills runs
7. **Permadeath is normal.** Every run teaches something.

---

*Full guidebook: GUIDEBOOK.md · Official: https://nethack.org/v367/Guidebook.html*

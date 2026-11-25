# NetHack Beginner's Tutorial

> Keys in this guide are the **NetHack defaults** (`number_pad:0`, vi-style movement).
> Doc set: this tutorial → [QUICKREF.md](QUICKREF.md) (1-page reference) → [CHEATSHEET.txt](CHEATSHEET.txt) (tiny crib sheet) → [TUTORIAL-FULL.md](TUTORIAL-FULL.md) / [GUIDEBOOK.md](GUIDEBOOK.md) (deep reference).

---

## 1. The Goal

Descend the Mazes of Menace, grab the **Amulet of Yendor** (below dungeon level 20), and climb back out alive. Most runs end long before that — **death is permanent**, the save file is deleted, and every new game has a freshly randomized dungeon. Dying is how you learn; expect it.

---

## 2. The Screen

Three regions: **messages** (top), **map** (middle), **status** (bottom).

```
You see here a long sword.                       <- messages
                    --------
                    |......|
                    |.....@|     @  = you
                    |......+     +  = closed door (walk into it to open)
                    -------.     .  = floor
                           ##### #  = corridor
                              .. $  = gold pile
                              d   d  = a small dog (likely your pet)
Dlvl:1 $:0 HP:16(16) Pw:2(2) AC:6 Xp:1 T:42 Hungry   <- status
```

**Message line.** Every event prints here. `--More--` means press **space** to continue. Missed one? `^P` (Ctrl+P) replays recent messages.

**Status line legend:**

| Field | Meaning |
|-------|---------|
| `Dlvl` | Dungeon level. You start at 1 and descend; the endgame is ~50 |
| `$` | Gold carried |
| `HP:cur(max)` | Hit points. Zero = dead, and dead is permanent |
| `Pw` | Spell power (mana). Ignore until you cast spells |
| `AC` | Armor class. **Lower is better** — naked is 10, good armor reaches 0 or below |
| `Xp` | Experience level |
| `T` | Turn counter (matters for hunger and corpse freshness) |
| trailing word | Hunger/condition state (see §7). Absent = fine |

---

## 3. Map Legend

The essentials — full glyph tables are in TUTORIAL-FULL §3.5.

| Glyph | Meaning | Glyph | Meaning |
|-------|---------|-------|---------|
| `@` | you (or another human) | `.` | floor |
| `d` `f` | dog / cat — early on, your pet | `#` | corridor |
| letters a–z, A–Z | monsters | `+` | closed door (or spellbook) |
| `$` | gold | `-` `\|` | walls (or open door) |
| `%` | food | `>` `<` | stairs down / up |
| `!` `?` `/` `=` `"` | potion, scroll, wand, ring, amulet | `^` | trap (once discovered) |
| `)` `[` `(` | weapon, armor, tool | `{` | fountain |
| `I` | remembered, unseen monster | `_` | altar |

Don't memorize — press `/` in game and type any symbol to ask what it is.

---

## 4. Moving Around

Movement is the vi-key diamond. Arrow keys also work for the four straight directions, but you **need the letters for diagonals**:

```
 y  k  u        y k u = diagonals up
  \ | /
 h--.--l        h = left   l = right
  / | \
 b  j  n        b j n = diagonals down      .  = wait one turn
```

Moving into a monster attacks it. Walking into a closed door opens it.

**Going faster:**

| Key | Effect |
|-----|--------|
| `H J K L Y U B N` (capitals) | Run that direction until something interesting |
| `G` + direction | Same idea, ignores corridor forks |
| `_` | **Travel**: pick any known tile, walk there automatically |
| `m` + direction | Move *without* picking up items or fighting (use to step past peacefuls) |
| `F` + direction | Force an attack, even at an empty-looking square |

**Numbers are count prefixes**, not movement: `10s` searches 10 times, `20.` rests 20 turns. This is the big difference from numpad mode.

**Three gotchas in vi mode:** kick is `^D` (not `k` — that moves up), loot is `#loot` (not `l` — that moves right), untrap is `#untrap` (not `u` — that moves up-right).

---

## 5. Looking at Things

Four "what is that?" commands:

```
:    describe what's on the floor under you
;    free-look — move the cursor to any tile, press . to describe it
/    "what is this symbol?" — type a glyph (e.g. d) for its meaning
i    inventory — what you're carrying
```

Unidentified items appear as "a scroll labeled XYZZY" or "a tin ring". **That's normal** — appearances are randomized every game. You learn what's what by using items, watching shop prices, or reading scrolls of identify.

---

## 6. Items and Inventory

**Pick up:** stand on an item and press `,`. Multiple items give a checklist — toggle with letters, or `A` for everything.

Your config **autopicks** the light, high-value classes: `$` gold, `!` potions, `?` scrolls, `/` wands, `=` rings. Heavy stuff (weapons, armor, food) stays put so you can decide. Press `@` to toggle autopickup — **do this inside shops**, where picking an item up means buying it.

**Check `i` often.** Each item gets a letter you'll use in other commands (`w a` = wield item `a`).

**What to do with each item type:**

| Symbol | Type | Command | Notes |
|--------|------|---------|-------|
| `)` | weapon | `w` wield | Also throwable with `t` |
| `[` | armor | `W` wear / `T` take off | Wear everything that fits; watch AC drop |
| `=` | ring | `P` put on / `R` remove | Burns hunger faster while worn |
| `"` | amulet | `P` / `R` | One at a time |
| `!` | potion | `q` quaff | Or throw at a monster |
| `?` | scroll | `r` read | Usually single-use, can be powerful |
| `/` | wand | `z` zap | Limited charges |
| `+` | spellbook | `r` study | Takes many turns — only in cleared rooms |
| `%` | food | `e` eat | Rations, fruit, corpses |
| `(` | tool | `a` apply | Lamps, lockpicks, bags, horns |
| `*` | gem/rock | — | Some valuable; rub on a touchstone to check |
| `$` | gold | (auto) | Picked up automatically |

Mnemonic: lowercase = put it **in** you or use it (`e`at, `q`uaff, `r`ead, `w`ield, `z`ap, `a`pply); uppercase = put it **on** you (`W`ear, `P`ut on, `T`ake off, `R`emove).

---

## 7. Fighting

**Melee:** walk into the monster — the attack is automatic. First make sure a weapon is **wielded** (`w` + letter); bare hands are dramatically weaker unless you're a Monk.

**Ranged:** `t` throws any item in a direction; `f` fires from your quiver (set it once with `Q`). Thrown daggers and darts are a strong opener for most classes.

**Flee:** just walk away — the monster gets one free swing. Stairs also work; descending breaks pursuit.

**Kill everything that moves** in the early dungeon. You need the XP, and many corpses are safe food.

---

## 8. Eating and Hunger

Press `e` to eat. Safest sources first: **food rations / fruit** (always safe), then **fresh corpses** (stand on one, `e`, confirm `y`).

**Hunger ladder** (status line, left to right is worse):

```
Satiated → (nothing) → Hungry → Weak → Fainting → Fainted → Starved (dead)
```

Eat *at* `Hungry`. `Weak` already drains Strength. Don't force food while `Satiated` — choking on a full stomach is a classic stupid death.

- **Safe early corpses:** newts, rats, geckos, kobolds, gnomes, jackals, lichens (lichen never rots)
- **Never eat:** your pet, anything human-shaped (cannibalism), kobold shamans (poison), bats (stun), or corpses older than ~50 turns
- **"You feel deathly sick"** after eating → `#pray` immediately; food poisoning kills in ~10–25 turns

---

## 9. Dungeon Features

| Key | Action | Context |
|-----|--------|---------|
| `s` | search adjacent tiles | Repeat (`10s`) at dead ends for hidden doors |
| `o` / `c` | open / close door | Walking into a door also opens it |
| `^D` | kick | Breaks locked doors (may hurt your leg) |
| `>` / `<` | descend / ascend stairs | Must be standing on the staircase |
| `^` | identify trap under cursor | After you've discovered it |
| `#force` | pry a lock with your weapon | Alternative to kicking chests |

Two door rules that confuse everyone: **you can't move diagonally through a doorway**, and a `+` that won't open may be locked (kick it) or a spellbook lying on the floor (`:` to check).

---

## 10. Extended Commands and Prayer

Press `#`, type the name (it autocompletes), Enter.

```
#pray    Emergency divine help — heals, cures sickness, ends starvation.
         Works when you're in genuine trouble, roughly once per ~1000 turns.
         Spamming angers your god. One crisis, one prayer.
#chat    Talk to an adjacent shopkeeper, priest, or your pet.
#offer   Sacrifice a fresh corpse on an altar — builds divine favor.
#loot    Open a container on your tile (chests, boxes).
#sit     Sit on a throne (random effect) — otherwise mostly useless.
#rub     Rub a lamp (rare genie wish) or a gem on a touchstone.
#enhance Spend skill credit after practicing a weapon class.
```

`#pray` is the one to remember — it's your get-out-of-jail card for poisoning, starvation, and near-death.

---

## 11. Survival Rules

- **`S` saves and quits**; relaunch to resume. Death deletes the save — there is no save-scumming.
- **BUC (Blessed/Uncursed/Cursed)** is the most important hidden property. Cursed weapons weld to your hand; cursed armor won't come off. Drop items on an altar (`_`) and step away to read all three at once. Until checked, don't wear/wield unknowns in dangerous spots.
- **Pets test for curses:** drop an item — pets avoid stepping on cursed ones.
- **Test unknown potions/scrolls in cleared rooms**, never next to monsters or shops.
- **Scrolls of identify are gold** — spend them on rings and wands first.
- **Wear all the armor you find.** AC stacks: helmet, body, cloak, boots, gloves, shield.
- **Feed your pet** fresh corpses to keep it loyal; it fights for you and out-levels you early.
- **Don't descend at low HP.** Rest (`20.` or search-in-place `20s`) until full first.

---

## 12. First 10 Turns Checklist

1. `i` — read your starting inventory, note the letters
2. `w` + letter — wield your weapon if not already wielded
3. `W` + letter — wear starting armor (watch AC drop)
4. Explore the starting room; autopickup grabs the valuables
5. `,` for anything left behind you want
6. `10s` at suspicious dead ends — hidden doors are common
7. Find the `>` stairs but don't descend until HP is full
8. Eat *before* `Hungry` turns into `Weak`
9. Keep the pet close — it's your best early weapon
10. When in real trouble: `#pray` (once)

---

## 13. Setup on This Machine

```
./play.sh              # vi-keys config (nethackrc-laptop, number_pad:0) — default
./play.sh numpad       # numpad config, if you ever want it back
```

Config details and option reference: [BACKEND.md](BACKEND.md).
In-game help: `?` for the menu, `&` then any key for "what does this do".

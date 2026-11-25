# NetHack 3.6.7 Guidebook

> Adapted from the official NetHack 3.6.7 Guidebook (nethack.org/v367/Guidebook.html).
> Original by Eric S. Raymond; edited and expanded for 3.6 by Mike Stephenson and others.

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [What Is Going On Here?](#2-what-is-going-on-here)
3. [The Screen](#3-the-screen)
   - [Status Lines (Bottom)](#status-lines-bottom)
   - [Message Line (Top)](#message-line-top)
   - [The Map](#the-map)
4. [Commands](#4-commands)
5. [Rooms and Corridors](#5-rooms-and-corridors)
   - [Doorways](#doorways)
   - [Traps](#traps)
   - [Stairs and Ladders](#stairs-and-ladders)
   - [Shops and Shopping](#shops-and-shopping)
6. [Monsters](#6-monsters)
   - [Fighting](#fighting)
   - [Your Pet](#your-pet)
   - [Steeds](#steeds)
   - [Bones Levels](#bones-levels)
7. [Objects](#7-objects)
   - [Curses and Blessings](#curses-and-blessings)
   - [Weapons](#weapons)
   - [Armor](#armor)
   - [Food](#food)
   - [Scrolls](#scrolls)
   - [Potions](#potions)
   - [Wands](#wands)
   - [Rings](#rings)
   - [Spellbooks](#spellbooks)
   - [Tools and Containers](#tools-and-containers)
   - [Amulets](#amulets)
   - [Gems](#gems)
   - [Large Rocks](#large-rocks)
   - [Gold](#gold)
8. [Conduct](#8-conduct)
9. [Options](#9-options)
10. [Scoring](#10-scoring)
11. [Explore Mode](#11-explore-mode)
12. [Credits](#12-credits)

---

## 1. Introduction

Your daily life has grown unfulfilling. Strange dreams of treasure-hunting, combat, and dark caverns have plagued you for months. The rumors grow louder: somewhere beyond the Valley of Gehennom, deep within the **Mazes of Menace**, lies the **Amulet of Yendor** — said to bring immortality to whoever claims it.

After one last night at the inn, you set off. The dungeon entrance is dark. Inside, something waits.

---

## 2. What Is Going On Here?

Your goal: **grab as much treasure as you can, retrieve the Amulet of Yendor, and escape the Mazes of Menace alive.**

### Roles

Your starting equipment, abilities, and playstyle depend on your chosen role:

| Role | Strengths | Starts With |
|------|-----------|-------------|
| **Archeologist** | Dungeon knowledge, stealth | Scientific tools |
| **Barbarian** | Exceptional strength | Hauberk, great two-handed sword |
| **Caveman/Cavewoman** | Exceptional strength | Neolithic weapons |
| **Healer** | Medicine, poison lore, gold | Healing tools |
| **Knight** | Devotion, superior armor | Full knightly kit |
| **Monk** | Unarmed combat, mobility | No armor — doesn't need it |
| **Priest/Priestess** | Spell and prayer ability | Clerical arms |
| **Ranger** | Archery, stealth, tracking | Ranged kit |
| **Rogue** | Locks, traps, stealth | Thief tools |
| **Samurai** | Speed, dual swords | Dai-sho |
| **Tourist** | Gold for shopping | Camera, credit card, food, maps |
| **Valkyrie** | Strength, cold resistance, stealth | Hardy northern kit |
| **Wizard** | Magic knowledge, affinities | Magic items, spells |

### Races

| Race | Traits |
|------|--------|
| **Dwarf** | Stocky, expert miner; high-quality metal armor |
| **Elf** | Agile, perceptive; fine craftwork |
| **Gnome** | Expert miner; secret mine complex exists in the dungeon |
| **Human** | No special abilities; eligible for any role |
| **Orc** | Barbaric, hates elves; inferior-quality equipment |

---

## 3. The Screen

The terminal has three regions: the **message line** (top), the **map** (middle), and the **status lines** (bottom).

---

### Status Lines (Bottom)

Two lines show your current state.

**Attributes** (first line):
- **St** — Strength: physical tasks, combat damage, carrying capacity
- **Dx** — Dexterity: hit chance, trap avoidance, object manipulation
- **Co** — Constitution: injury recovery and stamina
- **In** — Intelligence: spell-casting ability
- **Wi** — Wisdom: magical energy reserves
- **Ch** — Charisma: monster reactions, shop pricing

**Status** (second line):

| Field | Meaning |
|-------|---------|
| `Dlvl` | Current dungeon level |
| `$` | Gold carried |
| `HP:cur(max)` | Hit points — zero means dead |
| `Pw:cur(max)` | Spell power (mana) |
| `AC` | Armor class — **lower is better** |
| `Xp` | Experience level |
| `T` | Turn counter |
| Trailing word | Hunger state (absent = not hungry) |

**Hunger ladder:**
```
Satiated  →  (none)  →  Hungry  →  Weak  →  Fainting  →  Fainted  →  Starved
```

**Encumbrance:**
```
Unencumbered  →  Burdened  →  Stressed  →  Strained  →  Overtaxed  →  Overloaded
```

Other conditions (Blind, Conf, Hallu, Stun, Ill, etc.) appear as needed.

---

### Message Line (Top)

Every game event is reported here. When the line ends with `--More--`, press **space** to continue. Press **^P** (Ctrl+P) to replay recent messages.

---

### The Map

Default ASCII glyphs:

| Symbol | Meaning |
|--------|---------|
| `- \|` | Wall or open door |
| `.` | Floor tile or doorless passage |
| `#` | Corridor, iron bars, tree, or sink |
| `> <` | Stairs down / up |
| `+` | Closed door or spellbook |
| `@` | You (or another human) |
| `$` | Gold pile |
| `^` | Known trap |
| `)` | Weapon |
| `[` | Armor |
| `%` | Food |
| `?` | Scroll |
| `/` | Wand |
| `=` | Ring |
| `!` | Potion |
| `(` | Tool |
| `"` | Amulet or web |
| `*` | Gem or rock |
| `` ` `` | Boulder or statue |
| `I` | Remembered unseen monster |
| `d f u` | Dog / cat / pony (your pet) |

Use `/` to ask "what is this glyph?" and `;` for free-look (move cursor to any tile, press `.` to describe it).

---

## 4. Commands

Commands use one or two keystrokes. A numeric prefix repeats the command (e.g. `10s` searches ten times).

### Movement

| Keys | Effect |
|------|--------|
| `1`–`9` (numpad) or vi keys | Move one step in that direction |
| `5` | Wait one turn |
| Uppercase direction | Run until obstacle or interesting tile |
| `m` + direction | Move without picking up or fighting |
| `F` + direction | Force attack |
| `g` / `G` + direction | Go until something interesting |
| `_` | Travel: shortest path to a known tile |

### Key Actions

```
,   pick up          .   wait/rest        s   search adjacent
i   inventory        I   inventory by type
d   drop item        D   drop multiple    A   remove worn items
e   eat              w   wield weapon     W   wear armor
q   quaff potion     r   read             z   zap wand
t   throw            f   fire quiver      Q   set quiver ammo
P   put on ring/amulet  R   remove ring/amulet
T   take off armor   x   exchange weapons X   toggle two-weapon
a   apply tool       o   open door        c   close door
>   go down          <   go up            ^   describe trap
:   look at floor    ;   free-look        /   what is glyph?
\   show discovered  `   show one class   +   list spells
Z   cast spell       #   extended command
S   save and quit    ^P  messages         ^X  show attributes
^D  kick             ^R  redraw           ^T  teleport (if able)
@   toggle autopickup  O  set options     ?   in-game help
```

### Extended Commands (`#`)

Press `#`, type the name, press Enter:

```
#adjust     rearrange inventory letters
#annotate   label current dungeon level
#chat       talk to adjacent creature
#conduct    show voluntary challenge status
#dip        dip an object into a potion
#enhance    advance weapon or spell skills
#exploremode enter explore/discovery mode
#force      force a lock open
#invoke     use an object's special power
#jump       jump to an adjacent location
#kick       kick (same as ^D)
#loot       loot a container / remove saddle
#monster    use a polymorphed monster ability
#offer      sacrifice corpse on an altar
#overview   show dungeon overview
#pray       request divine help
#quit       exit without saving
#ride       mount or dismount a steed
#sit        sit on current tile
#travel     travel to a map location
#turn       turn undead
#twoweapon  toggle dual-wielding
#untrap     disarm a trap
#version    show version and compile options
```

---

## 5. Rooms and Corridors

The dungeon contains lit and dark areas. Illuminated rooms are fully visible; dark areas only render when you're adjacent. Walls and corridors remain on your map once explored. Hidden passages require `s` (search) to discover.

---

### Doorways

Door states: **open**, **closed**, **locked**, or **absent**.

- Walk into a closed door to open it, or press `o`
- `c` closes an open door
- Locked doors: use `a` with a key or lockpick, or kick with `^D`
- Open doors **cannot be entered diagonally** — approach straight on
- Doorless openings allow diagonal entry
- Most monsters cannot open doors (ghosts are an exception)
- Secret doors are hidden until found by searching

---

### Traps

Traps don't appear on the map until you trigger one, see something fall into one, or discover it with `s`. Monsters can also fall into traps — sometimes useful tactically.

The `#untrap` command lets you attempt to detect and disarm traps in containers.

One dungeon area features **Sokoban** puzzles: push boulders into pits to open the path forward.

---

### Stairs and Ladders

Most levels have two staircases: `<` (up) and `>` (down). Some branches — like the Gnomish Mines — dead-end, requiring you to backtrack.

When you use stairs, the current level is saved to disk. Returning reloads it; monsters on inactive levels don't act. Pets follow if adjacent when you descend; otherwise they're stranded.

---

### Shops and Shopping

A shopkeeper runs each commercial room. To buy:
1. Walk over the item (autopickup is fine)
2. Pay with `p`

Use `#chat` while standing on an item to ask its price before committing. Using or damaging an item before buying still incurs a charge.

To sell: drop an item on the floor. The shopkeeper may offer gold or decline.

**Important shop notes:**
- The tile just inside the doorway is considered **outside** the shop — stepping on it while leaving prompts payment
- Autopickup inside shops will buy items as you walk over them — turn it off with `@` before entering
- Shopkeepers run out of money and offer store credit instead; credit is shop-specific
- Closed shops don't reopen automatically
- Inventory never restocks
- The shopkeeper ignores other customers but watches you carefully

---

## 6. Monsters

Monsters you cannot see are not displayed on the screen. Use `/` to ask what a visible glyph is; `;` to examine any tile. `#chat` talks to adjacent creatures.

An `I` marker on the map is a **remembered, unseen monster** — your last known position for a creature that has moved out of sight.

---

### Fighting

Walk into a monster to attack. Many creatures ignore you unless provoked; the game prompts before attacking peaceful ones.

- `m` + direction — move without fighting (useful in tight situations)
- `F` + direction — force combat
- Fighting blind or against invisible monsters is possible but inaccurate

**Combat factors:** weapon type, enchantment/erosion, experience level, strength, dexterity, encumbrance, skill level, and the monster's AC. Some monsters are specifically vulnerable to silver, wood, iron, or holy weapons.

---

### Your Pet

You start with a companion: `d` small dog, `f` kitten, or `u` pony (depends on role).

- Pets follow you through stairs when adjacent
- They fight alongside you and gain experience from kills
- Dogs and cats feed themselves on fresh corpses; horses need vegetables
- Feed pets corpses from your inventory to keep them loyal
- Don't throw weapons through your pet
- **Pets as item testers:** drop an unidentified item — if the pet steps on it willingly, it's not cursed
- A pet separated too long may become wild

---

### Steeds

Some creatures can be ridden after saddling them with `a` (apply). Use `#ride` to mount or dismount. Remove a saddle with `#loot` while adjacent. Riding skill develops through `#enhance` like weapon skills.

---

### Bones Levels

Occasionally you enter a level where a previous adventurer (or a past version of yourself) died. Their ghost lingers — slow and weak, but their items are typically **cursed**. The monster that killed them may still be present.

---

## 7. Objects

Items are auto-collected by autopickup or grabbed with `,`. Each item gets an inventory letter (`a`, `b`, `c`...) used in commands like `w a` (wield item a).

**Carrying capacity** scales with Strength and Constitution:

```
Unencumbered → Burdened → Stressed → Strained → Overtaxed → Overloaded
```

Unidentified items show randomized descriptions (colors, materials, labels) that are consistent within one game. Use `#name` to label a type or individual item once you know what it is.

---

### Curses and Blessings

Every item has a **BUC status**: Blessed, Uncursed, or Cursed.

| Status | Effect |
|--------|--------|
| **Blessed** | Better than baseline (e.g., more damage vs. demons) |
| **Uncursed** | Normal function |
| **Cursed** | Negative effects; weapons weld to hand; armor can't be removed |

- Priests/Priestesses can sense BUC status innately
- **Altar test:** drop items on an altar and step off — the game reports each item's status
- **Pet test:** drop an item; if your pet steps on it, it's not cursed
- Scrolls of remove curse and holy water can fix cursed items
- Inventory shows "blessed"/"cursed" prefix when status is known; unknown status shows nothing

---

### Weapons

`)` — wield with `w`. Fighting bare-handed deals only 1–2 damage (Monks are the exception).

**Weapon types:**
- **Melee weapons** (swords, maces) — wielded with `w`
- **Thrown weapons** (spears, daggers) — thrown with `t` or fired
- **Ammunition** (arrows, bolts, rocks) — requires matching launcher

**Enchantment:** A weapon's `+` value affects both accuracy and damage. Positive enchantments help; negative ones hurt.

**Erosion:** Rust, rot, and burn damage reduce effectiveness. Magical repair is possible.

**Two-handed weapons** prevent shield use. One-handed weapons allow `x` to swap to an alternate.

**Commands:** `w` wield · `t` throw · `f` fire · `Q` set quiver · `x` exchange · `X` toggle two-weapon · `#enhance` improve skills

#### Throwing and Shooting

- `t` throws any object; pick item then direction
- `f` fires from your quiver (set with `Q`)
- Autoquiver replenishes the quiver automatically
- Some characters (especially Rangers) can fire multiple projectiles per turn
- Use a numeric prefix to cap shots: `2f` fires at most 2

#### Weapon Proficiency

Skills are grouped by weapon type (daggers, swords, polearms, etc.). Each role has a maximum skill per group.

| Level | Effect |
|-------|--------|
| Restricted | Cannot advance; penalties apply |
| Unskilled | Modest to-hit and damage penalty |
| Basic | No bonus or penalty |
| Skilled | Modest bonus |
| Expert | Higher bonus |
| Master / Grand Master | Unarmed combat only |

Use `#enhance` to advance skills when prompted. Total skill advancement across all categories is capped.

#### Two-Weapon Combat

Only some roles can do this. Setup with both weapons in hand, then `X` to toggle. Throwing, dropping, or losing either weapon reverts to single-weapon mode.

---

### Armor

`[` — wear with `W`; take off with `T`.

Armor Class (AC): **lower = better**. Base unarmored AC is 10.

| Armor | AC |
|-------|----|
| Dragon scale mail | 1 |
| Plate mail / crystal plate mail | 3 |
| Bronze plate mail, splint mail, banded mail | 4 |
| Dwarvish mithril-coat | 4 |
| Elven mithril-coat, chain mail | 5 |
| Scale mail, studded leather, ring mail | 7 |
| Leather armor | 8 |
| Leather jacket | 9 |
| No armor | 10 |

**Stack armor:** helmet + body + cloak + boots + gloves + shield all contribute.

One item per slot. Enchanted armor: a +1 chain mail gives AC 4 instead of 5.

**Cursed armor** carries negative enchantment and cannot be removed normally.

Some heavy armor interferes with spell casting.

**Commands:** `W` wear · `T` take off · `A` remove all

---

### Food

`%` — eat with `e`.

Without food, hunger leads to fainting and death. The hunger state appears in your status line.

**Safe foods:**
- Food rations, fruit, lembas — always safe
- Monster corpses — fresh only (within ~50 turns); the game warns about rotten ones

**Corpse effects:** eating some monsters grants special properties. You are what you eat.

**Danger foods:**
- Your own pet
- Human-shaped corpses (cannibalism has consequences)
- Corpses of poisonous monsters (kobold shamans, etc.)
- Rotten corpses (the warning may come too late)

**Vegetarian/vegan characters** avoid meat; forced consumption has side effects.

**Tins:** preserved food that never rots but takes time to open.

**If poisoned:** message says "You feel feverish" or "deathly sick" — `#pray` immediately. Illness kills in 8–25 turns.

---

### Scrolls

`?` — read with `r`. Most are consumed on use. Scrolls have whimsical nonsense labels ("READ ME", "THANX MAUD" backwards) randomized each game.

The **scroll of identify** is the most valuable — reveals item type, BUC status, charges, and enchantment.

A mail daemon may occasionally deliver a **scroll of mail** (system-dependent). Set `MAIL` env var to your mailbox, and optionally `MAILREADER` for your mail app.

---

### Potions

`!` — drink with `q`. Identified by liquid color, randomized each game.

- **Clear potions** are water
- **Blessed water** = holy water (devastating to undead; throw with `t`)
- **Cursed water** = unholy water

`#dip` submerges an object into a potion for various effects. Some potions have effects when thrown at monsters.

---

### Wands

`/` — zap with `z`. Each wand has limited charges, consumed one per use.

- Some wands need a direction; others don't
- Zap at yourself with `.` or `s` — usually unwise
- At 0 charges, zapping does nothing (rarely: one last "squeeze" destroys the wand)
- **Recharging** works but risks explosion; risk increases with each recharge
- **Breaking** (`a` apply on the wand): catastrophic magical release — last resort only

Fully identified wands show: `wand of X (recharge-count:charges)`. Charge count of `-1` means cancelled.

---

### Rings

`=` — put on with `P`; remove with `R`.

Rings provide lasting magical effects (unlike one-shot scrolls/potions). Wearing a ring accelerates hunger at a rate that varies by type. Only **two rings** can be worn at once — one per hand.

---

### Spellbooks

`+` — study with `r`. Reading transfers a spell to memory; each study attempt degrades the book until it's unreadable. Cursed or too-advanced spellbooks can harm you.

**Casting (`Z`):**
- Costs magical power (Pw) and increases hunger
- Spells cast well above your experience level may backfire
- Spell memory fades over time; rereading the book refreshes it
- Some spells need a direction; some need a target location; some affect you automatically

**Spell proficiency** improves through use and `#enhance`. Spell categories share the skill slot pool with weapon skills.

Some armor types restrict casting by limiting physical flexibility.

---

### Tools and Containers

`(` — apply with `a`.

Miscellaneous items with varied uses. Lamps have limited fuel. Flutes, horns, whistles, and other instruments have specific effects.

**Containers** (bags, boxes, chests):
- Open from the floor with `#loot`
- Open from inventory with `a` (apply)
- Chests may be locked — use a key, lockpick (`a`), kicking (`^D`), or `#force`
- Many chests are **trapped** — `#untrap` to detect and disarm before opening

---

### Amulets

`"` — put on with `P`; remove with `R`.

Like rings but typically more powerful. Only **one amulet** at a time, worn around the neck.

---

### Gems

`*` — various uses.

Valuable gems sell for significant gold and increase your final score. Plain rocks are worth little but work as sling ammunition or hand-thrown projectiles. Rub an unidentified gem on a **touchstone** (`#rub`) to identify it.

---

### Large Rocks

`` ` `` — push by walking into them.

Boulders and statues are heavy and mostly impractical. Push boulders to block corridors tactically. Some statues have unusual properties. Very large monsters throw boulders as weapons.

---

### Gold

`$` — auto-picked up.

Spends at shops and contributes to your final score. Some monsters react differently depending on how much gold you carry.

---

## 8. Conduct

Voluntary self-imposed restrictions tracked automatically by `#conduct`. Completing the game while maintaining one or more conducts is a mark of distinction.

| Conduct | Restriction |
|---------|-------------|
| **Foodless** | No solid food (beverages still allowed) |
| **Vegan** | No animal-derived foods |
| **Vegetarian** | No meat; eggs/dairy allowed |
| **Atheist** | No praying, sacrificing, or chatting with priests |
| **Weaponless** | No wielded weapons (throwing and spells still allowed) |
| **Pacifist** | Kill no monsters that grant experience |
| **Illiterate** | No reading scrolls or spellbooks |
| **Genocideless** | No genocide scrolls |
| **Polyformless** | No polymorph effects on yourself |
| **Wishless** | No wishes (wand of wishing, etc.) |

---

## 9. Options

Options customize NetHack behavior. Set them via:

1. **In-game:** `O` command — interactive menu
2. **Config file:** `~/.nethackrc` (Linux/Mac) or `NetHack.cnf` (Windows)
3. **Environment variable:** `NETHACKOPTIONS=option1,option2,...`

Key config areas:

| Area | What it controls |
|------|-----------------|
| Autopickup | Which item classes to auto-grab |
| Autopickup exceptions | Specific item names to include or exclude |
| Key bindings | Rebind any command key |
| Message types | Suppress, highlight, or stop on specific messages |
| Menu colors | Color-code inventory and menus |
| Status hilites | Highlight status fields at thresholds |
| Symbols | Replace ASCII glyphs with custom characters |
| Fruit | Name your preferred fruit food item |
| Name | Your character's name |
| Scores | How many scores to show at game end |

For the complete list of option names and syntax, press `O` in-game or consult the official Guidebook.

---

## 10. Scoring

Your score is calculated at the end of each run (win or loss) based on:

- **Gold** accumulated (carried + deposited)
- **Dungeon levels** reached
- **Experience level** attained
- **Valuable gems** carried out
- **Win bonus** for successfully ascending with the Amulet
- **Conduct bonuses** for self-imposed challenges maintained
- **Penalties** for dying, quitting, or certain actions

The high score list is shown at the end of a run. In-game, press `V` to view your game history.

---

## 11. Explore Mode

Explore mode (also called **discovery mode**) relaxes the permadeath rule. Enter it with `#exploremode` (default `M-x`). Confirmation required; default answer is No.

In explore mode, when you restore a saved game you can choose to **keep the save file** — making it possible to replay from that point multiple times.

### Debug Mode

Debug (wizard) mode provides testing commands: `#wizwish`, `#wizmap`, `#wizgenesis`, and others. Not available in normal play.

---

## 12. Credits

**Original Guidebook:** Eric S. Raymond

**Expanded for 3.6:** Mike Stephenson and others

**Publication date:** February 3, 2023

NetHack is the product of many years of collaborative development by the NetHack DevTeam and contributors across the wider community. Full credits are displayed in-game and on the NetHack website.

---

*Full official reference: https://nethack.org/v367/Guidebook.html*

# NetHack 3.6.7 — The Complete Tutorial

A comprehensive, organized guide covering every command, option, item type, dungeon area, and survival principle. Reference for the official Guidebook and built up with practical play knowledge.

---

## Table of Contents

1. [Introduction](#1-introduction)
   - 1.1 [What NetHack Is](#11-what-nethack-is)
   - 1.2 [The Goal](#12-the-goal)
   - 1.3 [Permadeath](#13-permadeath)
2. [Character Creation](#2-character-creation)
   - 2.1 [Roles (Classes)](#21-roles-classes)
   - 2.2 [Races](#22-races)
   - 2.3 [Alignment](#23-alignment)
   - 2.4 [Gender](#24-gender)
   - 2.5 [Picking a Beginner Combination](#25-picking-a-beginner-combination)
3. [The Screen](#3-the-screen)
   - 3.1 [The Three Regions](#31-the-three-regions)
   - 3.2 [Status Line Fields](#32-status-line-fields)
   - 3.3 [Hunger and Encumbrance Ladders](#33-hunger-and-encumbrance-ladders)
   - 3.4 [Conditions Glossary](#34-conditions-glossary)
   - 3.5 [Map Glyph Reference](#35-map-glyph-reference)
   - 3.6 [Monster Letters](#36-monster-letters)
4. [Movement](#4-movement)
   - 4.1 [Direction Keys](#41-direction-keys)
   - 4.2 [Run / Rush / Travel](#42-run--rush--travel)
   - 4.3 [Movement Prefixes](#43-movement-prefixes)
   - 4.4 [Doors and Diagonals](#44-doors-and-diagonals)
5. [Complete Command Reference](#5-complete-command-reference)
   - 5.1 [Single-Letter Commands](#51-single-letter-commands)
   - 5.2 [Ctrl-Key Commands](#52-ctrl-key-commands)
   - 5.3 [Symbol Commands](#53-symbol-commands)
   - 5.4 [Extended (#) Commands](#54-extended--commands)
   - 5.5 [Meta-Key Shortcuts](#55-meta-key-shortcuts)
   - 5.6 [number_pad Letter Aliases](#56-number_pad-letter-aliases)
   - 5.7 [Repeating Commands](#57-repeating-commands)
6. [Combat](#6-combat)
   - 6.1 [Melee](#61-melee)
   - 6.2 [Ranged: Throw, Fire, Quiver](#62-ranged-throw-fire-quiver)
   - 6.3 [Two-Weapon Combat](#63-two-weapon-combat)
   - 6.4 [Weapon Skills and #enhance](#64-weapon-skills-and-enhance)
   - 6.5 [Engraving Elbereth](#65-engraving-elbereth)
   - 6.6 [Ranged Tactics, Retreat, Choke Points](#66-ranged-tactics-retreat-choke-points)
   - 6.7 [Special Monsters and Their Tricks](#67-special-monsters-and-their-tricks)
7. [Inventory and Items](#7-inventory-and-items)
   - 7.1 [Picking Up and Autopickup](#71-picking-up-and-autopickup)
   - 7.2 [Item Letters and #adjust](#72-item-letters-and-adjust)
   - 7.3 [BUC: Blessed, Uncursed, Cursed](#73-buc-blessed-uncursed-cursed)
   - 7.4 [Identification Techniques](#74-identification-techniques)
   - 7.5 [Item Categories Overview](#75-item-categories-overview)
   - 7.6 [Weapons](#76-weapons)
   - 7.7 [Armor and AC](#77-armor-and-ac)
   - 7.8 [Food, Hunger, Corpses](#78-food-hunger-corpses)
   - 7.9 [Scrolls](#79-scrolls)
   - 7.10 [Potions](#710-potions)
   - 7.11 [Wands](#711-wands)
   - 7.12 [Rings](#712-rings)
   - 7.13 [Spellbooks and Spells](#713-spellbooks-and-spells)
   - 7.14 [Tools and Containers](#714-tools-and-containers)
   - 7.15 [Amulets](#715-amulets)
   - 7.16 [Gems and Rocks](#716-gems-and-rocks)
   - 7.17 [Gold](#717-gold)
8. [Magic and Religion](#8-magic-and-religion)
   - 8.1 [Spell Casting](#81-spell-casting)
   - 8.2 [Prayer (`#pray`)](#82-prayer-pray)
   - 8.3 [Altars and Sacrifice (`#offer`)](#83-altars-and-sacrifice-offer)
   - 8.4 [Donations to Priests](#84-donations-to-priests)
9. [Dungeon Structure](#9-dungeon-structure)
   - 9.1 [Dungeons of Doom (Main Branch)](#91-dungeons-of-doom-main-branch)
   - 9.2 [The Gnomish Mines](#92-the-gnomish-mines)
   - 9.3 [Sokoban](#93-sokoban)
   - 9.4 [The Quest](#94-the-quest)
   - 9.5 [Fort Ludios](#95-fort-ludios)
   - 9.6 [The Castle](#96-the-castle)
   - 9.7 [Gehennom and Vlad's Tower](#97-gehennom-and-vlads-tower)
   - 9.8 [The Invocation Ritual](#98-the-invocation-ritual)
   - 9.9 [Moloch's Sanctum and the Amulet](#99-molochs-sanctum-and-the-amulet)
   - 9.10 [The Ascension Run and the Planes](#910-the-ascension-run-and-the-planes)
10. [Shops and Economy](#10-shops-and-economy)
    - 10.1 [Buying](#101-buying)
    - 10.2 [Selling](#102-selling)
    - 10.3 [Price Identification](#103-price-identification)
    - 10.4 [Shop Etiquette](#104-shop-etiquette)
11. [Pets](#11-pets)
    - 11.1 [Starting Pets](#111-starting-pets)
    - 11.2 [Feeding and Loyalty](#112-feeding-and-loyalty)
    - 11.3 [Pets as Tools](#113-pets-as-tools)
    - 11.4 [Riding Steeds](#114-riding-steeds)
12. [Traps and Hazards](#12-traps-and-hazards)
13. [Conduct (Optional Challenges)](#13-conduct-optional-challenges)
14. [Configuration: `~/.nethackrc`](#14-configuration-nethackrc)
    - 14.1 [Where the File Lives](#141-where-the-file-lives)
    - 14.2 [File Syntax](#142-file-syntax)
    - 14.3 [Top-Level Statements](#143-top-level-statements)
    - 14.4 [Common Boolean Options](#144-common-boolean-options)
    - 14.5 [Common Compound Options](#145-common-compound-options)
    - 14.6 [Autopickup Exceptions](#146-autopickup-exceptions)
    - 14.7 [Key Bindings](#147-key-bindings)
    - 14.8 [Menu Colors and Status Hilites](#148-menu-colors-and-status-hilites)
    - 14.9 [A Recommended Starter Config](#149-a-recommended-starter-config)
15. [Scoring and Endgame](#15-scoring-and-endgame)
16. [Explore and Debug Modes](#16-explore-and-debug-modes)
17. [Survival Cheat Sheet](#17-survival-cheat-sheet)
18. [Glossary](#18-glossary)

---

## 1. Introduction

### 1.1 What NetHack Is

NetHack is a **roguelike**: a turn-based, single-player dungeon-crawling game played on a grid of ASCII characters. Each new game generates a fresh dungeon (about 50 levels deep). You control `@` and explore, fight, eat, cast spells, identify items, and try to survive.

The game is played entirely with the keyboard. Every action — opening a door, drinking a potion, praying to your god, kicking a sink — is a one- or two-key command.

### 1.2 The Goal

> **Retrieve the Amulet of Yendor from deep below, escape back to the surface, and offer the Amulet to your god on the Astral Plane.**

You "win" by **ascending**. This requires:

1. Descending all the way to the bottom of the dungeon
2. Performing the **invocation ritual** (Bell, Book, Candelabrum)
3. Defeating the High Priest of Moloch and taking the **Amulet of Yendor**
4. Climbing all the way back up
5. Crossing four **elemental planes** (Earth, Air, Fire, Water)
6. Reaching the **Astral Plane**, finding the altar of your god, and using `#offer` on the Amulet

A typical winning game takes thousands of turns and many hours of play. A typical losing game ends in 30 minutes.

### 1.3 Permadeath

When your character dies, the save is deleted. There is **no reload**. This is intentional — every decision matters because every decision is final.

Explore mode (`#exploremode`) relaxes this for learning purposes (see §16), but the standard game has no second chances.

---

## 2. Character Creation

You make four choices: **Role**, **Race**, **Alignment**, **Gender**. Each combination shapes your starting equipment, abilities, restrictions, and quest.

### 2.1 Roles (Classes)

| Role | Strength | Special | Notes |
|------|---------|---------|-------|
| **Archeologist** | Low | Speed, stealth | Pick-axe lets you dig anywhere |
| **Barbarian** | High | Poison resistance | Two-handed weapon start |
| **Caveman/Cavewoman** | Very high | Brute force | Crude weapons, weak magic |
| **Healer** | Low | Healing spells, gold | Stethoscope; great for new players |
| **Knight** | High | Lance + pony, jumping | Can `#turn` undead; chivalric code |
| **Monk** | Medium | Martial arts | Vegetarian; armor penalty |
| **Priest/Priestess** | Medium | BUC sense, `#turn` | Knows BUC of all items innately |
| **Ranger** | Medium | Volley fire, stealth | Bow + arrows; multi-shot |
| **Rogue** | Medium | Backstab, locks | Daggers, stealth |
| **Samurai** | High | Two-weapon combat | Katana + wakizashi + bow |
| **Tourist** | Very low | Camera, wishes | Hardest start; great endgame |
| **Valkyrie** | High | Cold resistance | Often recommended for first wins |
| **Wizard** | Low | Spells from start | Force bolt; magic missile |

### 2.2 Races

| Race | Notes |
|------|-------|
| **Human** | All roles. Up to lawful/neutral/chaotic. Baseline |
| **Dwarf** | Only Archeologist, Cavewoman, Valkyrie. Strong, lawful preference |
| **Elf** | Only Priest, Ranger, Wizard. Sleep resistance, infravision |
| **Gnome** | Only Archeologist, Caveman, Healer, Ranger, Wizard. Infravision |
| **Orc** | Only Barbarian, Ranger, Rogue, Wizard. Poison resistance, sees in dark |

### 2.3 Alignment

Lawful, Neutral, or Chaotic. Determines:
- Your patron deity and their opposite
- Which artifacts and prayers favor you
- How peaceful monsters react

Each role has restricted alignments — Knights are always lawful, Barbarians are neutral or chaotic, etc.

### 2.4 Gender

Mostly cosmetic: affects pronouns, the rank titles, and a few minor mechanics. Some roles have a gendered name (Cavewoman, Priestess, Valkyrie is always female).

### 2.5 Picking a Beginner Combination

For a first run, pick one of these:

- **Valkyrie, Dwarf, Lawful** — strong starting weapon (long sword), cold resistance, hard to kill
- **Samurai, Human, Lawful** — bow start lets you fight at range
- **Wizard, Elf, Chaotic** — magic missile is strong from level 1; sleep resistance saves lives
- **Healer, Gnome, Neutral** — slow but tanky; healing spell is amazing

---

## 3. The Screen

### 3.1 The Three Regions

```
You see here a long sword.                   ← message line (top)
                    --------
                    |......|
                    |.<....|##              ← map (middle)
                    |...@..|
                    |.d....+
                    --------
Player the Stripling   St:18 Dx:14 Co:16 In:7 Wi:11 Ch:7 Lawful
Dlvl:1 $:0 HP:16(16) Pw:2(2) AC:6 Xp:1/0 T:1                ← status (bottom)
```

The map area is at most 21 lines × 80 columns regardless of terminal size.

### 3.2 Status Line Fields

| Field | Meaning |
|-------|---------|
| **Rank** | Class title that increases with experience (Stripling, Fighter, Champion...) |
| **St** | Strength (3–18; 18/01–18/99 for very strong; up to 25) |
| **Dx** | Dexterity (3–25) |
| **Co** | Constitution (3–25) |
| **In** | Intelligence (3–25) |
| **Wi** | Wisdom (3–25) |
| **Ch** | Charisma (3–25; affects shop prices) |
| **Alignment** | Lawful / Neutral / Chaotic |
| **Dlvl** | Current dungeon level |
| **$** | Gold openly carried |
| **HP** | Hit points: `current(max)`. Zero = dead |
| **Pw** | Power (mana) for spells |
| **AC** | Armor Class. **Lower is better.** Negative is great |
| **Xp** | Experience: `level/points` (with `showexp` option) |
| **T** | Turn counter (with `time` option) |

### 3.3 Hunger and Encumbrance Ladders

```
Hunger:       Satiated → (none) → Hungry → Weak → Fainting → Fainted → Starved
Encumbrance:  Unencumbered → Burdened → Stressed → Strained → Overtaxed → Overloaded
```

Eat by `Hungry`. `Weak` already costs Strength. `Satiated` in combat can choke and kill you.

Burdened slows movement; Stressed slows it more; Overtaxed makes you collapse.

### 3.4 Conditions Glossary

**Fatal** (will kill you if not cured):
- `Stone` / `Petrifying` — turning to stone (lizard corpse, acid potion, prayer)
- `Slime` — turning into green slime (fire, prayer)
- `Strngl` — being strangled (cursed amulet of strangulation; remove fast)
- `FoodPois` — food poisoning (`#pray`, eunicorn horn)
- `TermIll` — terminal illness (`#pray`, holy water)

**Non-fatal**:
- `Blind` — can't see; engrave with fingers, drink/cure
- `Deaf` — can't hear; wears off
- `Stun` — random movement; wears off
- `Conf` — confused; spells/scrolls misfire; wears off
- `Hallu` — hallucinating; monsters appear randomized

**Movement**:
- `Lev` — levitating (can't pick up, can't descend stairs)
- `Fly` — flying
- `Ride` — mounted on a steed

### 3.5 Map Glyph Reference

| Symbol | Meaning |
|--------|---------|
| `-` `\|` | Wall, open door, or grave |
| `.` | Floor, ice, doorless doorway |
| `#` | Corridor, iron bars, tree, sink, or drawbridge |
| `>` | Stairs down |
| `<` | Stairs up |
| `+` | Closed door OR spellbook |
| `@` | You (or another human) |
| `$` | Pile of gold |
| `^` | Known trap |
| `)` | Weapon |
| `[` | Armor |
| `%` | Edible item |
| `?` | Scroll |
| `/` | Wand |
| `=` | Ring |
| `!` | Potion |
| `(` | Tool |
| `"` | Amulet OR spider web |
| `*` | Gem or rock |
| `` ` `` | Boulder or statue |
| `0` | Iron ball |
| `_` | Altar, or iron chain |
| `{` | Fountain |
| `}` | Water, moat, or lava |
| `\` | Throne |
| `I` | Last known position of an unseen monster |

### 3.6 Monster Letters

| Letter | Class | Examples |
|--------|-------|---------|
| `a` | Ant / insect | giant ant, killer bee |
| `b` | Blob | acid blob, gelatinous cube |
| `c` | Cockatrice | (touch = stone!) |
| `d` | Dog / canine | jackal, your pet dog |
| `e` | Floating eye | (don't melee — paralysis) |
| `f` | Cat / feline | kitten, large cat |
| `g` | Gnome / gremlin | gnome, gnomish wizard |
| `h` | Dwarf | dwarf, dwarvish hero |
| `i` | Imp / minor demon | imp, manes |
| `j` | Jelly | blue jelly, brown pudding |
| `k` | Kobold | kobold, kobold lord |
| `l` | Leprechaun | (steals gold) |
| `m` | Mimic | (looks like an item!) |
| `n` | Nymph | (steals items!) |
| `o` | Orc | orc, hill orc |
| `p` | Piercer | rock piercer (drops from ceiling) |
| `q` | Quadruped | rothe (dangerous early) |
| `r` | Rat | rat, giant rat |
| `s` | Spider / snake | giant spider |
| `t` | Trapper / lurker | (camouflaged ceiling) |
| `u` | Pony / unicorn | horn = altar BUC |
| `v` | Vortex | air vortex (stuns) |
| `w` | Worm | long worm (multi-tile!) |
| `x` | Grid bug | (free XP) |
| `y` | Light / yellow | yellow light blinds |
| `z` | Zruty | tough humanoid |
| `A` | Angel | aligned servant |
| `B` | Bat | starfish, giant bat |
| `C` | Cocky/Cyclops | giant, ettin |
| `D` | Dragon | red, white, blue, etc. |
| `E` | Elemental | air, earth, fire, water |
| `F` | Fungus / lichen | (lichen corpses never rot) |
| `G` | Gnome | gnome lord, gnomish king |
| `H` | Giant | hill giant, fire giant |
| `I` | Invisible monster marker | not a real letter |
| `J` | Jabberwock | (very tough) |
| `K` | Kobold | kobold shaman (poison!) |
| `L` | Lich | lich, demilich |
| `M` | Mummy | mummy, kobold mummy |
| `N` | Naga | naga hatchling, golden naga |
| `O` | Ogre | ogre, ogre king |
| `P` | Pudding | black pudding (split when hit!) |
| `Q` | Quantum mechanic | random teleport |
| `R` | Rust monster | (eats your iron items!) |
| `S` | Snake | (poisonous) |
| `T` | Troll | (regenerates, eat corpse!) |
| `U` | Umber hulk | (confuses gaze) |
| `V` | Vampire | drains XP |
| `W` | Wraith / ghost | wraith eat = +1 level |
| `X` | Xan / xorn | xorn passes through walls |
| `Y` | Ape / yeti | yeti, gorilla |
| `Z` | Zombie | various zombies |
| `&` | Demon | various |
| `:` | Lizard | (lizard corpse cures stone) |
| `'` | Golem | iron, clay, etc. |
| `;` | Sea monster | giant eel (drowns!) |

---

## 4. Movement

### 4.1 Direction Keys

```
Vi keys:           Numpad:
  y  k  u            7  8  9
   \ | /              \ | /
  h- . -l            4- . -6
   / | \              / | \
  b  j  n            1  2  3
```

`5` (numpad) or `.` (vi) = wait one turn.

Set with the `number_pad` option (see §14).

### 4.2 Run / Rush / Travel

| Key | Effect |
|-----|--------|
| `YUHJKLBN` (uppercase) | Run until obstacle or interesting tile |
| `g` + direction | Go until something interesting |
| `G` + direction | Same as `g`, but ignore corridor forks |
| `Ctrl` + direction | Same as `G` |
| `_` | **Travel**: pick a known map tile, walk there automatically |

### 4.3 Movement Prefixes

| Prefix | Effect |
|--------|--------|
| `m` + direction | Move without picking up or fighting |
| `F` + direction | Force attack (even into empty tile) |
| `M` + direction | Move far without picking up |

`m` is essential for safely walking past peaceful monsters or invisible-but-known foes you don't want to fight.

### 4.4 Doors and Diagonals

- Walk into a closed door to open it (with `autoopen` on, the default)
- Open doors **cannot be entered diagonally** — go straight in
- Doorless openings allow diagonal entry
- `c` to close a door behind you (defensive)
- `o` to open without walking in

---

## 5. Complete Command Reference

Every default key binding in NetHack 3.6.7. Defaults assume `number_pad:0`.

### 5.1 Single-Letter Commands

```
a   apply tool                      A   remove all worn items
c   close door                      C   call (name) monster/object
d   drop                            D   drop multiple by category
e   eat                             E   engrave on floor
f   fire from quiver                F   force-attack prefix
g   go-until prefix                 G   go ignoring forks prefix
h j k l y u b n   movement          H J K L Y U B N   run movement
i   inventory                       I   inventory by type
j   (jump if number_pad)            
k   (kick if number_pad)            
l   (loot if number_pad)            
m   move-without-fight prefix       M   move-far-no-pickup prefix
N   (name if number_pad)            
o   open door                       O   set options
p   pay shop bill                   P   put on (ring/amulet)
q   quaff (drink) potion            Q   set quiver
r   read scroll/spellbook           R   remove ring/amulet
s   search (repeat several)         S   save and quit
t   throw                           T   take off armor
u   (untrap if number_pad)          
v   show version                    V   show game history
w   wield weapon (w- = bare hand)   W   wear armor
x   exchange primary/secondary      X   toggle two-weapon combat
z   zap wand                        Z   cast spell
```

### 5.2 Ctrl-Key Commands

```
^A   redo previous command          ^O   show dungeon overview
^C   panic quit                     ^P   replay messages
^D   kick                           ^R   redraw screen
^T   teleport (if able)             ^X   show character attributes
^Z   suspend game (UNIX only)
```

### 5.3 Symbol Commands

```
.    wait/rest                      ?    in-game help menu
,    pick up                        /    "what is this glyph?"
:    look at floor                  ;    examine glyph at location
@    toggle autopickup              ^    describe trap under you
)    show wielded weapon            [    show worn armor
=    show worn rings                "    show worn amulet
(    show tools in use              *    show all equipment
$    count gold                     +    list spells
\    show discovered objects        `    show one object class
!    shell escape                   #    extended command
&    "what does this key do?"
<    go up stairs                   >    go down stairs
```

### 5.4 Extended (#) Commands

Press `#`, type the name (autocompletes after a few letters), Enter. Most have meta-key shortcuts (§5.5).

**Movement / interaction:**
```
#chat       talk to adjacent creature
#ride       mount or dismount steed
#sit        sit on the current tile
#travel     travel to map location (also _)
#jump       jump (some classes / boots)
#monster    use polymorphed-form ability
```

**Combat / equipment:**
```
#enhance    advance weapon/spell skills
#twoweapon  toggle dual-wielding (also X)
#turn       turn undead (Priest/Knight)
```

**Objects / containers:**
```
#adjust     reassign inventory letter
#dip        dip an object into a potion
#force      force a lock with weapon
#invoke     activate an artifact's power
#loot       open container under you OR remove saddle
#name       name a monster/object/type
#tip        tip a container to dump contents
#untrap     try to disarm a trap (or chest)
#wipe       wipe your face (after pie/blindness)
#rub        rub a lamp/touchstone/stone
```

**Religion:**
```
#pray       pray to your god
#offer      sacrifice corpse on altar
```

**Information:**
```
#annotate   add a one-line note to current level
#conduct    show maintained voluntary challenges
#overview   show dungeon overview (also ^O)
#terrain    show bare map (no monsters/objects)
#version    show compile options
#whatdoes   describe a key
#whatis     describe a glyph
#?          help for extended commands
#herecmdmenu / #therecmdmenu   show menu of contextual actions
```

**Game state:**
```
#exploremode  switch to explore mode (one-way)
#quit         quit without saving
#save         save and quit (also S)
#suspend      suspend (also ^Z)
```

**Debug-mode only** (not in normal play):
```
#wizwish, #wizmap, #wizgenesis, #wizidentify, #wizlevelport,
#wizdetect, #wizbury, #wizintrinsic, #wizrumorcheck, #wizsmell,
#wizwhere, #wmode, #panic, #polyself, #levelchange,
#lightsources, #seenv, #stats, #timeout, #vanquished, #vision
```

### 5.5 Meta-Key Shortcuts

If your terminal sends ESC+key as meta, these speed up common extended commands.

```
M-?  #?              M-2  #twoweapon       M-a  #adjust
M-A  #annotate       M-c  #chat            M-C  #conduct
M-d  #dip            M-e  #enhance         M-f  #force
M-i  #invoke         M-j  #jump            M-l  #loot
M-m  #monster        M-n  #name            M-o  #offer
M-O  #overview       M-p  #pray            M-q  #quit
M-r  #rub            M-R  #ride            M-s  #sit
M-t  #turn           M-T  #tip             M-u  #untrap
M-v  #version        M-w  #wipe
```

In xterm-style terminals, the `altmeta` option lets ESC + key act as Meta + key.

### 5.6 number_pad Letter Aliases

When `number_pad` is on (your hands sit on the numpad for movement), these letters become extended-command shortcuts:

```
h  #help        j  #jump        k  #kick
l  #loot        N  #name        u  #untrap
```

### 5.7 Repeating Commands

A numeric prefix repeats:

```
10s         search ten times (find hidden doors faster)
20.         rest 20 turns (regen HP)
3f          fire at most 3 from quiver
```

With `number_pad` on, prefix the count with `n`:  `n10s`.

ESC cancels a count or prefix.

---

## 6. Combat

### 6.1 Melee

Walk into a monster to attack. The hit is automatic.

```
w <letter>   wield item (must be wielded for full damage)
w -          fight bare-handed (Monks excepted)
A            unwield + remove armor (multi-select)
```

**Hit chance** depends on: weapon type, enchantment, your experience level, Strength, Dexterity, encumbrance, weapon skill, and the monster's AC. Some monsters are vulnerable to specific materials (silver vs. demons, holy water vs. undead).

**Erosion** (rust, rot, burn, corrode) reduces effectiveness. A `+1 long sword` is better than a plain one; a `rusty long sword` is worse.

### 6.2 Ranged: Throw, Fire, Quiver

```
t <letter> <dir>   throw any item in a direction
Q <letter>         set quiver (ammo on standby)
f <dir>            fire from quiver (no item prompt)
```

**Launchers and ammo:**
- Bow (`)`) shoots arrows (`/`)
- Crossbow shoots crossbow bolts
- Sling shoots rocks and gems

You **must wield the launcher** to get the to-hit and damage bonus when shooting matched ammo.

**Volley fire**: Rangers and high-skilled archers fire multiple shots per turn. Cap with `2f` to fire at most 2.

`autoquiver` option auto-fills your quiver from inventory when it empties.

### 6.3 Two-Weapon Combat

Only some roles can dual-wield (Barbarian, Ranger, Samurai, Valkyrie...).

Setup options:
- Both weapons correct already: `X` toggles two-weapon mode
- Primary right, secondary missing: `x` (swap), `w <secondary>`, `x` (swap back)
- Easier: enable `pushweapon` option, then `w <secondary>`, `w <primary>`

Two-weapon mode incurs an accuracy penalty. Dropping or losing either weapon reverts to single-weapon.

### 6.4 Weapon Skills and #enhance

Weapons are grouped (daggers, broadswords, polearms, bows, etc.). Each role has a max skill per group.

| Skill | Effect |
|-------|--------|
| Restricted | Can't advance; penalties |
| Unskilled | Modest hit/damage penalty |
| Basic | No bonus |
| Skilled | Modest bonus |
| Expert | Higher bonus |
| Master / Grand Master | Bare-hand combat only (Monks) |

After enough hits with a weapon, the game says "you feel more confident." Use `#enhance` to spend the skill point. Total advancement is capped — choose wisely.

### 6.5 Engraving Elbereth

`E -` writes in dust with your fingers. The word **"Elbereth"** scares most monsters away from melee — they will not attack you in hand-to-hand combat while standing on Elbereth (with a few exceptions: humans, elves, minotaurs, the Riders).

```
E - Elbereth <Enter>
```

Engraved Elbereth is rubbed away by:
- Your own attacks from that tile
- Casting spells
- Many movement actions

It's a desperation move that buys you turns to heal or escape.

### 6.6 Ranged Tactics, Retreat, Choke Points

- **Choke point**: stand in a corridor so monsters can attack you only one at a time
- **Stairs**: descending breaks line of sight — emergency escape
- **Doors**: close them behind you (`c`); most monsters can't open them
- **Boulders**: push (walk into) into corridors to block pursuit
- **Drink potions of speed early** — extra moves per turn = enormous advantage

### 6.7 Special Monsters and Their Tricks

| Monster | Glyph | Threat | Counter |
|---------|-------|--------|---------|
| Floating eye | `e` (blue) | Paralyzes melee attackers | Throw items, blind yourself, wear free-action ring |
| Cockatrice | `c` (yellow) | Touch = stone | Wear gloves, use ranged, carry lizard corpse |
| Medusa | `@` | Gaze = stone | Wear blindfold, fight blind |
| Nymph | `n` | Steals item, teleports | Kill fast or avoid |
| Leprechaun | `l` | Steals gold | Avoid carrying gold near them |
| Soldier ant | `a` | Fast, poison | Engrave Elbereth, retreat |
| Mind flayer | `h` (purple) | Drains Int permanently | Avoid until late game |
| Mimic | `m` | Disguised as item | Be cautious in shops |
| Yellow light | `y` | Explodes, blinds | Kill at range |
| Trapper | `t` | Floor/ceiling camouflage | Searches help |

---

## 7. Inventory and Items

### 7.1 Picking Up and Autopickup

```
,        pick up items at current tile (multi-select if many)
@        toggle autopickup on/off
```

`pickup_types` (in your config) controls which classes are auto-picked. Default is "all". A common setting is `pickup_types:$"=/!?+` (gold, amulets, rings, wands, potions, scrolls, spellbooks).

`autopickup_exception` lines refine further (see §14.6).

**Carrying capacity** scales with Strength + Constitution. Going past `Burdened` slows you.

### 7.2 Item Letters and #adjust

Each picked-up item gets a letter `a`–`z`, `A`–`Z`. Letters are used in commands: `q b` quaffs item `b`.

`#adjust` reassigns letters so your most-used items stay in convenient slots:
```
#adjust k → b     moves item k to slot b
3#adjust k → b    moves 3 of item k from k to b (splits stack)
```

### 7.3 BUC: Blessed, Uncursed, Cursed

The single most important hidden attribute of every item.

| State | Effect (general) |
|-------|------------------|
| **Blessed** | Better than normal — extra damage, longer duration, more reliable |
| **Uncursed** | Normal |
| **Cursed** | Worse than normal — weapon welds to hand, armor stuck on, scrolls/potions worse |

**Cursed gear is dangerous.** Symptoms:
- *"the X welds itself to your hand"* — cursed weapon
- *"You can't"* on `T` (take off) — cursed armor
- *"You feel light-headed"* on putting on a ring — cursed
- A ring or amulet you can't `R` (remove)

**Cures:**
- Scroll of remove curse
- Holy water (cursed → uncursed; uncursed → blessed)
- `#pray` when in trouble
- Some artifacts

### 7.4 Identification Techniques

Most items start unidentified — random color/material/label per game.

| Technique | How |
|-----------|-----|
| **Use ID** | Quaff/zap/read; if effect is obvious, it's identified for that game. Risky |
| **Scroll of identify** | Reads on selected items. Blessed identifies more at once. Most efficient ID method |
| **Price ID** | Item base price (in shops) maps to a small list of possible types. See §10.3 |
| **Altar ID (BUC)** | Drop items on an altar, step off; game reports BUC of each |
| **Priest ID (BUC)** | Pay a priest for an "alignment check" — they'll tell you BUC of inventory |
| **Pet ID (curse only)** | Drop item near pet; if pet steps on it, it's not cursed |
| **Wear/wield** | Putting on uncursed armor or wielding uncursed weapon shows enchantment |

Innate: **Priests** see BUC of every item automatically.

### 7.5 Item Categories Overview

| Symbol | Class | Action | Key |
|--------|-------|--------|-----|
| `)` | Weapon | wield / throw | `w` / `t` |
| `[` | Armor | wear / take off | `W` / `T` |
| `=` | Ring | put on / remove | `P` / `R` |
| `"` | Amulet | put on / remove | `P` / `R` |
| `!` | Potion | quaff / dip / throw | `q` / `#dip` / `t` |
| `?` | Scroll | read | `r` |
| `/` | Wand | zap / break | `z` / `a` |
| `+` | Spellbook | study / cast | `r` / `Z` |
| `%` | Food | eat | `e` |
| `(` | Tool | apply | `a` |
| `*` | Gem/rock | throw / sell | `t` / shop |
| `` ` `` | Boulder/statue | push / break | walk / kick |
| `0` | Iron ball | (chained punishment) | — |
| `_` | (Altar — terrain) | sacrifice / drop | `#offer` / `d` |
| `$` | Gold | (auto-collect) | — |

### 7.6 Weapons

**Weapon types** (selected):
- **Edged**: dagger, knife, short sword, long sword, broadsword, two-handed sword, scimitar, katana, sabre
- **Blunt**: club, mace, morning star, war hammer, aklys, flail
- **Polearms**: lance, glaive, halberd, bardiche
- **Pierce**: spear, javelin, trident, pick-axe (also a tool!)
- **Ranged**: bow + arrows, crossbow + bolts, sling + rocks
- **Thrown**: dagger, dart, shuriken, javelin, boomerang

A weapon's "plus" (`+1 long sword`, `-2 mace`) modifies hit and damage. `?` enchant weapon raises it; cursed enchant lowers.

**Damage types** matter — silver vs. demons/lycanthropes, blessed vs. undead.

### 7.7 Armor and AC

**Armor Class**: 10 = unarmored; **lower is better**; can go negative.

Slots (one item per slot):

| Slot | Examples |
|------|----------|
| Body suit | leather armor, chain mail, plate mail, dragon scale mail |
| Cloak | cloak, elven cloak, oilskin cloak, cloak of magic resistance |
| Shirt | T-shirt, Hawaiian shirt (under suit) |
| Helmet | helmet, dwarvish iron helm, helm of brilliance |
| Gloves | leather gloves, gauntlets of power |
| Boots | low boots, jumping boots, speed boots, levitation boots |
| Shield | small shield, large shield, shield of reflection |

**AC totals stack.** A typical mid-game setup is AC 0 to -5; endgame is -20 or lower.

**Selected base AC values:**

| Armor | AC |
|-------|----|
| Dragon scale mail | 1 |
| Plate mail / crystal plate mail | 3 |
| Bronze plate mail, splint mail, banded mail, dwarvish mithril-coat | 4 |
| Elven mithril-coat, chain mail | 5 |
| Orcish chain mail, scale mail | 6 |
| Dragon scales, studded leather, ring mail | 7 |
| Orcish ring mail, leather armor | 8 |
| Leather jacket | 9 |
| (none) | 10 |

A `+1 chain mail` gives AC 4 instead of 5. Cursed armor often has negative enchantment.

**Beware**: wearing heavy armor restricts spell casting (failure rate up).

### 7.8 Food, Hunger, Corpses

Eat with `e`. Sources from safest to riskiest:

1. **Rations / fruit / lembas / cram** — always safe
2. **Tins** — safe but slow to open (`a` to apply)
3. **Fresh corpses** — within ~50 turns of the kill

**Dangerous corpses to eat:**

- Old (rotten) — game warns "Ulch! That food was rotten!"
- Kobold shamans, K (poisonous)
- Yellow molds (hallucinate)
- Bats — stunned
- Acid blobs — acid damage
- Cockatrice/chickatrice — turn to stone
- Wraiths — drain XP **(WAIT: wraith corpse = +1 level! Always eat!)**
- Lichens — never rot (carry them)
- Lizards — cure stoning **(carry one!)**
- Floating eyes — telepathy when blind (very useful)

**Cannibalism / pet-eating** has bad aftereffects (alignment hit, prayer cooldown).

If poisoned ("you feel feverish") → `#pray` immediately. Death in 8–25 turns.

### 7.9 Scrolls

`r` to read. Most are consumed.

**Notable scrolls:**

| Scroll | Effect |
|--------|--------|
| Identify | Identifies items in inventory (1 if uncursed, more if blessed) |
| Enchant weapon / armor | +1 to weapon/armor |
| Magic mapping | Reveals current level's terrain |
| Genocide | Eliminate a monster species permanently |
| Charging | Recharge a wand (risky) |
| Remove curse | Uncurse items |
| Teleportation | Random teleport on this level |
| Confuse monster | Next melee hit confuses target |
| Scare monster | Drops scare-monster on floor (like Elbereth tile) |
| Earth | Drop boulders around you |
| Fire | Damage yourself unless fire-resistant |
| Mail | (mail daemon) — flavor / sometimes useful |
| Punishment | Curses you with iron ball + chain (avoid) |
| Amnesia | Forget known item identifications |

**Tip**: blessed scrolls of identify identify multiple items at once, picked from a menu.

### 7.10 Potions

`q` to quaff. `#dip` an object into one for special effects.

**Notable potions:**

| Potion | Effect |
|--------|--------|
| Healing / Extra healing / Full healing | Restore HP (and max HP) |
| Speed | Permanent intrinsic speed (huge!) |
| Object detection | See all objects on level |
| Monster detection | See all monsters on level |
| Gain ability / Gain level | Boost stat / level |
| Enlightenment | Reveal info about your character |
| Holy water (blessed water) | Bless any item via `#dip` |
| Acid / Hallucination / Sleep / Confusion | Bad if drunk |
| Booze | Drunk; flavor |
| Polymorph | Change form (controlled with poly control ring) |

**Throwing a potion** at a monster has its own effect (acid burns, holy water burns undead, sleep puts to sleep).

### 7.11 Wands

`z` to zap. Each wand has limited charges.

**Wand types:**

| Wand | Direction? | Effect |
|------|------------|--------|
| Wishing | No | One wish per charge — usually 1–3 charges. **Best item in game** |
| Death | Yes | Kills target (most monsters) |
| Polymorph | Yes | Changes target's form |
| Cancellation | Yes | Removes magic from target |
| Teleportation | Yes | Teleports target |
| Striking | Yes | Damage |
| Magic missile | Yes | Damage |
| Cold / Fire / Lightning | Yes | Elemental damage; reflects off shields |
| Sleep | Yes | Puts target to sleep |
| Slow monster | Yes | Reduces monster speed |
| Speed monster | Yes | (Zap at self for permanent speed!) |
| Make invisible | Yes | (Zap at self for permanent invisibility) |
| Digging | Down/dir | Dig through walls or floors |
| Light | No | Lights area |
| Probing | Yes | See monster HP/inventory |
| Secret door detection | No | Reveals doors |
| Locking / Opening | Yes | Lock/unlock doors and chests |
| Nothing | (no effect) | |

**Engrave-test**: `E` with an unidentified wand engraves a substance that hints at type. Wand of digging digs a hole. Wand of fire/cold/lightning produces special engraving.

**At 0 charges** zapping does nothing (rarely "squeeze" destroys it). Recharging risks explosion (chance grows with each recharge).

### 7.12 Rings

`P` put on, `R` remove. Two slots (one per finger).

**Notable rings:**

| Ring | Effect |
|------|--------|
| Conflict | All nearby monsters fight each other |
| Free action | Immune to paralysis (vs floating eyes, sleep) |
| Polymorph control | Choose form when polymorphed |
| Slow digestion | Hunger 1/3 speed (extends late game!) |
| Regeneration | Faster HP regen (but more hunger) |
| Increase damage / accuracy | Combat boost |
| Levitation | Can't pick up, can't go down stairs |
| Hunger | Speeds up hunger (curse this off!) |
| Adornment | Charisma boost (better shop prices) |
| Teleportation / Teleport control | Random / controlled tp |
| See invisible | See `I` markers |
| Stealth | Don't wake sleeping monsters |
| Warning | Sense nearby monsters |

Wearing a ring usually accelerates hunger.

### 7.13 Spellbooks and Spells

`r` to study (transfer knowledge). `Z` to cast a known spell. `+` to list spells.

**Studying risks:**
- Spellbook may be cursed (pet test it!)
- Spell too high-level for your skill (wizard tower of skill)
- Cursed → confusion, paralysis, sometimes death
- Eventually books become unreadable

**Casting:**
- Costs Pw (mana)
- Costs nutrition
- Failure rate shown in `+` listing
- Spell knowledge fades over time — restudy

**Spell categories** (skills shared with weapon skill pool):
- Attack: magic missile, force bolt, fireball
- Healing: cure light/blindness, healing, extra healing
- Divination: identify, magic mapping, detect monsters/food
- Enchantment: charm monster, sleep, confuse monster
- Clerical: turn undead, remove curse, protection
- Escape: teleport away, jumping, levitation
- Matter: dig, polymorph, cancellation
- Special: cast at self with `.` direction

### 7.14 Tools and Containers

`a` to apply.

**Common tools:**

| Tool | Use |
|------|-----|
| Pick-axe | Dig walls/floors (dig down with `a` then `>`) |
| Lock pick / skeleton key / credit card | Unlock doors and chests |
| Magic lamp | Wish on it (rub) |
| Oil lamp / lantern | Light source (limited fuel) |
| Crystal ball | Identify monster type (with risk) |
| Magic whistle | Teleport pets to you |
| Tinning kit | Preserve corpses as tins |
| Stethoscope | Show monster HP |
| Bag of holding | Reduces weight of contents! |
| Bag of tricks | Random monster summon |
| Sack / oilskin sack | Storage; oilskin is waterproof |
| Mirror | Confuse monsters, scare medusa |
| Camera | Blind monsters (Tourist start) |
| Magic marker | Write scrolls (very rare and valuable) |
| Towel | Wipe face after blindness/pies |
| Saddle | Mount a steed |
| Tin opener | Open tins faster |
| Horn (various) | Frost, fire, etc. |

**Containers** (`#loot` or `a`):

| Container | Notes |
|-----------|-------|
| Sack | Basic storage |
| Oilskin sack | Waterproof — protects scrolls/spellbooks from water |
| Bag of holding | Reduces weight — but never put another bag inside! |
| Bag of tricks | Releases random hostile monster |
| Large box / chest | Heavy; may be locked, may be trapped |

`#untrap` to check chests for traps before opening.
`#force` to force a lock with your weapon.

### 7.15 Amulets

`P` / `R`. One slot.

**Notable amulets:**

| Amulet | Effect |
|--------|--------|
| Life saving | Auto-resurrect once on death |
| Reflection | Reflects rays (cold, fire, magic missile) |
| Magical breathing | Don't drown / suffocate |
| ESP / telepathy | See monsters by mind |
| Strangulation | Cursed — strangles you. Remove fast! |
| Restful sleep | Puts you to sleep periodically (avoid) |
| Yendor | The win condition |

### 7.16 Gems and Rocks

`*`. Some gems are worth thousands of gold; others are worthless glass.

**Identification**: rub a gem on a touchstone (`#rub`) to identify it. Or sell to a shop and check the offer.

Real gems contribute to score. Throw with sling for damage.

### 7.17 Gold

`$`. Used in shops, bribing demons, donations. Counted in score. Some monsters react to gold (leprechauns steal it; nymphs covet shiny things).

---

## 8. Magic and Religion

### 8.1 Spell Casting

```
+        list known spells (level, skill group, fail %, retention)
Z        cast a spell (then pick spell, then direction if needed)
Z .      cast at self (where appropriate)
```

**Failure** = wasted Pw + turn. Reduce by:
- Higher Wisdom (Priest/Wizard) or Intelligence (others)
- Lighter armor (heavy armor adds penalty)
- Higher skill via `#enhance`
- Better luck

### 8.2 Prayer (`#pray`)

Pray to your god. Effective **only when you are in trouble** and it has been long enough since your last help.

**Cooldown**: ~800–1000 turns. Praying without a real crisis or while still in cooldown angers your god (smiting, lightning bolt, undeserved curses).

**Major troubles** (god will fix):
- HP critically low (≤1/7 max or ≤5)
- Stoning, sliming, strangling
- Food poisoning, terminal illness
- Stuck in lava
- Fainting / starving
- Cursed lev/strangulation amulets
- Petrification

**Minor troubles** (god *might* fix):
- Hungry (not Weak)
- Blind, stunned, hallucinating, confused
- Stuck/punished
- Cursed worn equipment

**The god's reaction:**
- Pleased: heal, uncurse, restore stats, sometimes a gift
- Indifferent: nothing happens
- Angry: lightning bolt, smiting, equipment destruction, cursing

Don't pray on:
- Cross-aligned altar (you'll be smited)
- After cannibalism or eating your pet (alignment hit)
- During cooldown unless you're really dying

### 8.3 Altars and Sacrifice (`#offer`)

`_` is an altar. Each altar has an alignment (Lawful, Neutral, Chaotic).

**Uses for altars:**

1. **BUC test**: drop items on altar, step off — game reports BUC of every item
2. **Sacrifice corpses (`#offer`)** on a same-alignment altar:
   - Earn favor with your god
   - May receive gifts (artifact weapons!)
   - May convert cross-aligned altars to your alignment
   - Sacrificing same-race corpse = bad
   - Sacrificing high-XP monster = better favor
3. **Convert altars**: sacrifice on a cross-aligned altar; success converts it to your alignment, failure summons an angry monster

**Co-aligned priests** in Mine Town will:
- Identify BUC of all your items (donate gold)
- Bless water at altars (save holy water)

### 8.4 Donations to Priests

Walk up to a priest, `#chat`, agree to donate. Cost is 400 × your Xp level. Reveals BUC of your entire inventory and gives you protection (lower AC over time).

---

## 9. Dungeon Structure

The Mazes of Menace are organized as a tree of branches.

### 9.1 Dungeons of Doom (Main Branch)

The main downward path. About 25 levels.

| Approx. Level | Feature |
|----|---------|
| 1 | Start |
| 2–4 | Branch staircase to **Gnomish Mines** (one extra `>`) |
| 5–9 | **Oracle** level (consultation: minor or major) |
| 6–10 | Branch staircase to **Sokoban** — but it goes **UP**! |
| 11–16 | **Big Room** sometimes; **Quest portal** appears (need Xp 14) |
| ~14 | Rare **Fort Ludios** vault portal |
| 21 | **Medusa's level** (with stone-gaze risk) |
| 22–25 | **Castle** — drawbridge, moat, magical chest |
| Beyond | **Valley of the Dead** — entrance to **Gehennom** |

### 9.2 The Gnomish Mines

Branches off DLvl 2–4. Roughly 5–10 levels deep.

- Open caverns instead of rooms
- Many gnomes, dwarves, gnomish wizards
- **Mine Town** (about Lvl 5–7 of Mines): shops, priest, watchmen
  - Don't anger watchmen — they all attack
  - Shops: general, weapon, food, lighting, etc.
  - Priest = donation + holy water creation
- **Mine's End** (bottom): pile of gems, **luckstone** (very valuable)

### 9.3 Sokoban

Branches **up** off DLvl 6–10. Four pre-built levels.

Push boulders into pits/holes per traditional Sokoban rules. Solving carefully gives Luck bonus; cheating (rolling boulders past holes, killing monsters with boulder pushes) gives Luck penalty.

**Reward at the top**: choose **bag of holding** OR **amulet of reflection**. (Amulet is usually better for first-time players.)

### 9.4 The Quest

Each role has a unique 3-level Quest dungeon, accessible from a portal in DoD around Lvl 11–16. You need:

- Experience level **14**
- **Quest leader's quest** (talk to your role's quest leader on the portal level)
- Aligned with your role

**Three Quest levels:**
1. The Home — your quest leader, allies
2. The Hall of corridors — intermediate monsters
3. The Goal — face the **Quest nemesis** and win the **Quest artifact**

**Quest artifacts** (gifted upon victory):

| Role | Artifact |
|------|----------|
| Archeologist | Orb of Detection |
| Barbarian | Heart of Ahriman |
| Caveman | Sceptre of Might |
| Healer | Staff of Aesculapius |
| Knight | Magic Mirror of Merlin |
| Monk | Eyes of the Overworld |
| Priest | Mitre of Holiness |
| Ranger | Longbow of Diana |
| Rogue | Master Key of Thievery |
| Samurai | Tsurugi of Muramasa |
| Tourist | Platinum Yendorian Express Card |
| Valkyrie | Orb of Fate |
| Wizard | Eye of the Aethiopica |

### 9.5 Fort Ludios

Optional bonus area accessed via a magic portal in a vault on DLvl ~12–14. Very rare.

- Loaded with gold, monsters, and powerful items
- **Croesus** (the shopkeeper) sells the best stuff
- Soldiers are tough; sleep gas and bombs

### 9.6 The Castle

DLvl ~26. End of the main downward dungeon. Surrounded by a moat (drawbridge or levitation/swimming required).

**Inside the Castle:**
- Throne room with **wand of wishing** (in a chest!)
- Some random monsters
- **Trapdoor** to Valley of the Dead

The wand of wishing is a top reason to reach the Castle. Wish for **gray dragon scale mail** for magic resistance.

### 9.7 Gehennom and Vlad's Tower

Below the Castle: the Valley of the Dead, then a long maze descending through Gehennom.

- Mostly mazes; navigation slow without dig/teleport
- Many demons, including demon lords
- **Asmodeus**, **Baalzebub**, **Juiblex**, **Yeenoghu** as demon lords

**Vlad's Tower** branches off Gehennom — 3 levels with **Vlad the Impaler** at the top. He guards the **Candelabrum of Invocation** (one of the three invocation items).

Near the bottom of Gehennom, the **Wizard of Yendor** wanders. He carries the **Book of the Dead** (another invocation item) and steals the Amulet from you on the way back if he can.

### 9.8 The Invocation Ritual

To open the way to Moloch's Sanctum (the level holding the Amulet), you must perform the invocation on the **invocation level** (the level just above Sanctum).

You need three items:

| Item | Where |
|------|-------|
| **Bell of Opening** | Inside the Castle's chest |
| **Candelabrum of Invocation** | Vlad's Tower (top, with Vlad) |
| **Book of the Dead** | Carried by the Wizard of Yendor |

Plus **seven candles** (any kind — wax or tallow), all attached to the Candelabrum.

Procedure on the invocation level:

1. Be at the same spot as a vibrating square (a hidden trap-like square)
2. Light all 7 candles attached to the Candelabrum
3. `a` apply the Bell, then `r` read the Book

If everything is correct, a downstaircase opens to **Moloch's Sanctum**.

### 9.9 Moloch's Sanctum and the Amulet

The bottom of the dungeon. Guarded by the **High Priest of Moloch** and tough demon servants.

The Amulet of Yendor sits on an altar in the Sanctum.

Pick up the Amulet (`,`) and the ascension begins.

### 9.10 The Ascension Run and the Planes

Climb back up. The Wizard of Yendor will repeatedly try to steal the Amulet. Angels of your god will help; angels of opposing gods may attack.

After climbing all the way out of the dungeon back to DLvl 1, you find a magic portal to the elemental planes:

| Plane | Hazard |
|-------|--------|
| **Earth** | Maze; Earth elementals; xorns |
| **Air** | Floating; Air elementals; lightning |
| **Fire** | Lava; Fire elementals; demons |
| **Water** | Bubbles of air in water; aquatic monsters |
| **Astral** | Three altars (Lawful, Neutral, Chaotic), the **Riders** (Death, Famine, Pestilence), and your god's altar |

On Astral: find your god's altar (only one of the three is yours), `#offer` the Amulet, and you ascend!

The **Riders** are extremely tough — Death is especially feared. Fight them or sneak past with speed/teleport/digging.

---

## 10. Shops and Economy

### 10.1 Buying

- Walk in. Items on the floor are the merchandise
- Pick one up — shopkeeper notes the price as your "bill"
- Pay with `p` before leaving
- The tile inside the door counts as **outside**: stepping on it triggers payment

### 10.2 Selling

- Drop item inside shop (`d`)
- Shopkeeper offers gold or declines (must be a class they buy)
- Accidentally dropping = shop claims it for free; buy back at full price

### 10.3 Price Identification

The base price of an item narrows down its possible types. Examples:

- Unidentified ring at 100gp = could be teleportation, regeneration, slow digestion, etc. (3–5 candidates)
- Unidentified wand at 175gp = striking, sleep, slow monster, others
- Scroll at 50gp = identify, light, gold detection, food detection, magic mapping, others

Charisma and shopkeeper attitude affect the actual price; the **base price** matters for ID. There are wiki tables for this.

### 10.4 Shop Etiquette

- Turn off **autopickup** (`@`) before entering
- Pay before leaving — shopkeepers get violent
- Don't kill the shopkeeper unless you're prepared (very strong)
- Locking yourself in with the shopkeeper is a death sentence
- Use `#chat` on items to price-check before pickup
- Don't drop and pick up rapidly inside — that's "buying and selling" which loses gold

---

## 11. Pets

### 11.1 Starting Pets

| Class | Pet |
|-------|-----|
| Most | small dog (`d`) or kitten (`f`) |
| Knight | pony (`u`) |
| Priest | small dog (`d`) |
| (set with `pettype` option) | "cat", "dog", "horse", or "none" |

Name with `C` (call). Not much functional difference among species early.

### 11.2 Feeding and Loyalty

- Throw food at your pet (`t`) to feed. Builds loyalty
- Dogs/cats hunt corpses themselves
- Horses need vegetables
- A starving pet may turn wild
- A pet that hits you (e.g. by stepping on Elbereth) becomes wild

### 11.3 Pets as Tools

- **Item BUC test**: drop unknown item, watch your pet:
  - Steps on it → not cursed
  - Avoids stepping on it → cursed
  - May not work for items pet wants to grab
- **Combat assistance**: pet attacks adjacent enemies, gains XP
- **Theft**: a pet next to a shopkeeper can steal items if you do it carefully (advanced; risky)

### 11.4 Riding Steeds

- Use `a` (apply) saddle on adjacent rideable creature
- `#ride` to mount/dismount
- Riding skill via `#enhance`
- Knight starts with a saddled pony

---

## 12. Traps and Hazards

Traps appear as `^` once known. Discover with:
- Triggering them (often bad)
- Searching with `s` (need adjacency, repeat several times)
- Some scrolls/potions/rings reveal traps

**Common traps:**

| Trap | Effect |
|------|--------|
| Arrow / dart | Damage, possibly poison |
| Bear trap | Stuck in place several turns |
| Pit / spiked pit | Stuck; spikes may poison |
| Trap door | Drops you 1+ levels |
| Teleport trap | Random teleport on level |
| Level teleport | Random level |
| Magic trap | Random magical effect |
| Polymorph trap | Polymorphs you |
| Sleeping gas | Sleep |
| Anti-magic field | Drains Pw, hurts spell users |
| Rust trap | Rusts your iron |
| Squeaky board | Wakes monsters |
| Web | Stuck (try to break or wait) |
| Falling rock | Damage |
| Land mine | Big damage; destroys items |
| Magic portal | Travel to another dungeon area |

`#untrap` attempts to disarm an adjacent trap or check a chest.

---

## 13. Conduct (Optional Challenges)

Tracked automatically. View with `#conduct`.

| Conduct | Restriction |
|---------|------------|
| **Foodless** | No solid food (drinks OK; pray for food OK) |
| **Vegan** | No animal products. Lichens/jellies/blobs OK |
| **Vegetarian** | No meat. Eggs, dairy, jellies OK |
| **Atheist** | No `#pray`, `#offer`, `#turn`, `#chat` with priests |
| **Weaponless** | No wielded weapons. Throwing/spells OK |
| **Pacifist** | No killing for XP |
| **Illiterate** | No reading scrolls/spellbooks/engravings |
| **Genocideless** | No `?` of genocide use |
| **Polyselfless / Polypileless** | No polymorph effects |
| **Wishless** | No wishes |
| **Artifact-wishless** | No wishing for artifacts |

---

## 14. Configuration: `~/.nethackrc`

### 14.1 Where the File Lives

| OS | Location |
|----|----------|
| Linux / macOS | `~/.nethackrc` |
| Windows | `%USERPROFILE%\NetHack\3.6\.nethackrc` |
| MS-DOS | `defaults.nh` next to `nethack.exe` |

### 14.2 File Syntax

- Lines starting with `#` = comments
- Empty lines ignored
- `[section]` markers + `CHOOSE=` for randomized configs
- `OPTIONS=opt1,opt2,...` for option lists
- One option per line is fine and clearer

### 14.3 Top-Level Statements

| Statement | Purpose |
|-----------|---------|
| `OPTIONS=` | Set boolean or compound options |
| `BIND=key:command` | Rebind keys |
| `AUTOPICKUP_EXCEPTION=` | Refine autopickup |
| `MENUCOLOR=` | Color menu lines matching pattern |
| `MSGTYPE=` | Show/hide/stop on certain messages |
| `SOUND=` / `SOUNDDIR=` | Audio mappings |
| `SYMBOLS=` | Replace ASCII glyphs |
| `CHOOSE=` | Randomly pick a `[section]` |
| `HACKDIR` `SAVEDIR` `LEVELDIR` `BONESDIR` | File locations |

### 14.4 Common Boolean Options

Prefix with `!` or `no` to turn off. Example: `OPTIONS=!legacy,autopickup`.

| Option | Default | Effect |
|--------|---------|--------|
| `autopickup` | on | Auto-pick items walked over |
| `autoopen` | on | Walk into closed doors to open |
| `autodig` | off | Wielding pick-axe + walking into wall = dig |
| `autoquiver` | off | Auto-fill quiver when empty |
| `autodescribe` | on | Describe tile under cursor when picking location |
| `bones` | on | Save/load bones files (other adventurers' deaths) |
| `cmdassist` | on | Hint at common mistakes |
| `confirm` | on | Confirm attacks on peaceful creatures |
| `dark_room` | on | Show dark room areas |
| `extmenu` | off | Pop-up menu for `#` commands |
| `fixinv` | on | Inventory letters stay sticky |
| `force_invmenu` | off | Always show menu on item-prompt |
| `help` | on | Show "More info?" prompt for `/` |
| `hilite_pet` | off | Visually distinguish pets |
| `hilite_pile` | off | Mark stacks of items |
| `hitpointbar` | off | HP bar behind name (TTY/Win) |
| `legacy` | on | Show intro message at start |
| `lit_corridor` | off | Show lit corridor squares |
| `mail` | on | Mail daemon delivers scroll of mail |
| `mention_walls` | off | Comment when walking into walls |
| `menucolors` | off | Enable MENUCOLOR rules |
| `nudist` | off | Start with no armor |
| `perm_invent` | off | Always-visible inventory pane (windowed) |
| `pickup_thrown` | on | Auto-pick items you've thrown |
| `pushweapon` | off | `w` pushes old weapon to alternate |
| `rest_on_space` | off | Space = rest one turn |
| `safe_pet` | on | Confirm before attacking pets |
| `showexp` | off | Show XP points in status |
| `showrace` | off | Show as race glyph instead of role |
| `showscore` | off | Show approximate score in status |
| `silent` | on | Suppress terminal beeps |
| `sortpack` | on | Group inventory by type |
| `sparkle` | on | Sparkle effect on resisted attacks |
| `splash_screen` | on | Windows GUI splash |
| `standout` | off | Boldface monsters and `--More--` |
| `time` | off | Show turn counter |
| `tombstone` | on | Tombstone graphic on death |
| `travel` | on | Allow `_` travel command |
| `verbose` | on | More commentary |
| `implicit_uncursed` | on | Hide "uncursed" prefix |

### 14.5 Common Compound Options

| Option | Example | Effect |
|--------|---------|--------|
| `align` | `align:lawful` | Pick alignment (or just `l`) |
| `boulder` | `boulder:0` | Display boulders as `0` |
| `catname` | `catname:Felix` | Name your kitten |
| `dogname` | `dogname:Rex` | Name your dog |
| `horsename` | `horsename:Trigger` | Name your horse |
| `disclose` | `disclose:+i +v na ng nc no` | What to reveal at game end |
| `fruit` | `fruit:mango` | Custom fruit name |
| `gender` | `gender:male` | Pick gender |
| `menustyle` | `menustyle:full` | Menu style: traditional/combination/full/partial |
| `msghistory` | `msghistory:50` | Number of recallable messages |
| `msg_window` | `msg_window:r` | Message recall display: s/c/f/r |
| `name` | `name:Alaric-V` | Character name + role suffix (-V = Valkyrie) |
| `number_pad` | `number_pad:0` | Movement keys: 0/1/2/3/4/-1 |
| `packorder` | `packorder:")[%?+!=/(*\`0_"` | Inventory display order |
| `paranoid_confirmation` | `paranoid_confirmation:pray attack Remove` | Require "yes" on certain prompts |
| `pettype` | `pettype:cat` | Choose pet species |
| `pickup_burden` | `pickup_burden:S` | Don't pick up past Stressed |
| `pickup_types` | `pickup_types:$"=/!?+` | Autopickup classes |
| `pile_limit` | `pile_limit:5` | Pile message threshold |
| `playmode` | `playmode:explore` | Force explore/debug mode |
| `race` | `race:dwarf` | Pick race |
| `role` | `role:Valkyrie` | Pick class |
| `runmode` | `runmode:walk` | Map update speed: teleport/run/walk/crawl |
| `scores` | `scores:5 top/own` | Score list at end |
| `sortloot` | `sortloot:full` | Sort behavior |
| `suppress_alert` | `suppress_alert:3.6.7` | Suppress version-change alerts |
| `symset` | `symset:default` | Symbol set name |
| `whatis_coord` | `whatis_coord:c` | Coordinate display style |

### 14.6 Autopickup Exceptions

Lines after the patterns. `<` prefix = always pick up; `>` prefix = never.

```
AUTOPICKUP_EXCEPTION="<*arrow"
AUTOPICKUP_EXCEPTION=">*corpse"
AUTOPICKUP_EXCEPTION=">* cursed*"
```

Result: always grab arrows, never grab corpses, never grab known-cursed items.

### 14.7 Key Bindings

```
BIND=^X:getpos.autodescribe
BIND=v:loot
BIND={:menu_first_page
```

Format: `BIND=key:command`. Key forms:
- `x` literal
- `^X` Ctrl+X
- `M-x` Meta/Alt+X
- Three-digit ASCII code

Bind extended commands by their name (`loot`, `pray`, `enhance`, etc.). Use `nothing` to unbind.

### 14.8 Menu Colors and Status Hilites

Color matching menu lines:

```
OPTIONS=menucolors
MENUCOLOR=" blessed "=green
MENUCOLOR=" cursed "=red
MENUCOLOR=" uncursed "=cyan
MENUCOLOR="holy water"=light-cyan&bold
```

Highlight low HP:
```
OPTIONS=hitpointbar
OPTIONS=statushilites:10
OPTIONS=hilite_status:hp/<=33%/red&bold
OPTIONS=hilite_status:hp/<=66%/yellow
OPTIONS=hilite_status:hunger/Hungry/yellow
OPTIONS=hilite_status:hunger/Weak/red&bold
```

### 14.9 A Recommended Starter Config

```
# ~/.nethackrc — beginner-friendly
OPTIONS=name:Hero, role:Valkyrie, race:Dwarf, gender:female, align:lawful
OPTIONS=catname:Mittens, dogname:Rex
OPTIONS=fruit:mango

# Display
OPTIONS=color, lit_corridor, dark_room
OPTIONS=hilite_pet, hilite_pile
OPTIONS=hitpointbar
OPTIONS=time, showexp, showscore
OPTIONS=standout, sparkle

# Inventory and pickup
OPTIONS=autopickup, pickup_types:$"=/!?+
AUTOPICKUP_EXCEPTION="<*arrow"
AUTOPICKUP_EXCEPTION=">* cursed*"

# UI behavior
OPTIONS=menustyle:full, sortpack, sortloot:full
OPTIONS=msghistory:80, msg_window:r
OPTIONS=runmode:walk
OPTIONS=paranoid_confirmation:pray attack Remove wand-break

# Status hilites (need statushilites:N where N>0)
OPTIONS=statushilites:10
OPTIONS=hilite_status:hp/<=33%/red&bold
OPTIONS=hilite_status:hp/<=66%/yellow
OPTIONS=hilite_status:hunger/Hungry/yellow
OPTIONS=hilite_status:hunger/Weak/red&bold
OPTIONS=hilite_status:hunger/Fainting/red&blink

# Menu colors for inventory
OPTIONS=menucolors
MENUCOLOR=" blessed "=green
MENUCOLOR=" cursed "=red
MENUCOLOR=" uncursed "=cyan
MENUCOLOR="holy water"=light-cyan&bold

# Disclose everything at game end
OPTIONS=disclose:+i +a +v +g +c +o
```

---

## 15. Scoring and Endgame

Your score reflects:

- **Experience gained** during the run
- **Loot accumulated** (gold + valuable gems)
- **Dungeon depth** explored
- **How the game ended**:
  - **Quit alive** (`#quit`) — keep all gold
  - **Died** in the dungeon — only 90% of your gold counts (corpse looters take a cut)
  - **Ascended** — huge bonus, score multiplied

The `tombstone` graphic appears on death (toggle via option). The `disclose` option controls what info is revealed at game end.

`nethack -s all` shows the local high score list.

A typical winning ascension scores in the millions; a typical loss in the thousands.

---

## 16. Explore and Debug Modes

**Explore mode** (`-X` command line, `playmode:explore` config, or `#exploremode` in-game):
- Permadeath relaxed: dying offers a "die anyway?" prompt
- Save files keepable on restore
- Starting in explore gives a wand of wishing
- Score not posted to high score list

**Debug mode (wizard mode)** (`-D` command line, `playmode:debug` config):
- Many debug-mode-only commands (`#wizwish`, `#wizmap`, `#wizgenesis`, etc.)
- Often restricted to particular usernames / character names
- Falls back to explore mode if not allowed

Use explore for learning. Don't use debug unless you're debugging.

---

## 17. Survival Cheat Sheet

The most important rules, in order:

1. **Check BUC before equipping.** Altars, priests, scrolls of identify. Pet test (food on item; pet steps = not cursed).
2. **Eat by `Hungry`, never past `Weak`.** Carry rations and lichen corpses.
3. **`#pray` only in real crisis.** Once per ~1000 turns.
4. **Don't melee floating eyes (`e`).** Throw items. Wear free action ring. Or kill with a pet.
5. **Cockatrices (`c`) turn you to stone on touch.** Wear gloves. Use ranged. Carry a lizard corpse.
6. **`s` searches** — repeat 5–10 times at suspicious dead ends.
7. **Wand of wishing wishes**: gray dragon scale mail, blessed +3 silver dragon scale mail, blessed greased fixed +3 gauntlets of power, blessed +5 holy spear of light...
8. **Engrave Elbereth (`E - Elbereth`)** when overwhelmed. Buys you turns.
9. **Never read unidentified scrolls or quaff unidentified potions near stairs/escape routes.** Some teleport.
10. **Save the scroll of identify for rings and wands first.**
11. **In Sokoban: solve cleanly.** Cheating costs Luck.
12. **The Castle has a wand of wishing.** Plan for it.
13. **Carry a unicorn horn.** Cures stun, confusion, blindness, sickness, hallucination.
14. **Carry holy water.** Bless arbitrary items by `#dip`.
15. **Permadeath is a feature.** Each death is a lesson — no replay needed.

---

## 18. Glossary

| Term | Meaning |
|------|---------|
| **AC** | Armor Class. Lower is better. |
| **Altar** | `_` floor tile of a god's alignment. BUC test, sacrifice, conversion. |
| **Amulet** | The Amulet of Yendor — game-winning artifact at the bottom |
| **Ascend / Ascension** | Win the game by offering the Amulet on Astral |
| **Bones level** | Dungeon level loaded from a previous adventurer's death |
| **BUC** | Blessed / Uncursed / Cursed status of every item |
| **Branch** | Side dungeon (Mines, Sokoban, Quest, etc.) |
| **Conduct** | Self-imposed challenge (vegan, atheist, weaponless...) |
| **DLvl / DoD** | Dungeon Level / Dungeons of Doom |
| **Elbereth** | Engraved word that scares most monsters in melee |
| **Engraving** | Text on the floor (`E`); permanent (carved) or temporary (dust) |
| **Gehennom** | Lower dungeon, mostly mazes; route to Sanctum |
| **HP / Pw** | Hit Points / Power (mana) |
| **Identify** | Reveal an item's true type |
| **Invocation** | Ritual with Bell/Book/Candelabrum to open Sanctum |
| **Pet** | Starting companion; helps fight, tests BUC |
| **Permadeath** | Dying ends the run for good |
| **Polymorph** | Change form (item or self) |
| **Quaff** | Drink (`q`) |
| **Quest** | Class-specific 3-level branch with artifact reward |
| **Riders** | Death, Famine, Pestilence on the Astral Plane |
| **Sanctum** | Bottom dungeon level holding the Amulet |
| **Scroll** | Single-use magical paper |
| **Sokoban** | Boulder-pushing puzzle branch (upstairs from DoD) |
| **Tin** | Canned food; safe but slow to open |
| **Wand of wishing** | Best item; grants wishes |
| **Yendor** | The Amulet's eponym; the Wizard of Yendor is your nemesis |
| **Zap** | Use a wand (`z`) |

---

*Companion documents in this directory:*
- **TUTORIAL.md** — short beginner's guide
- **GUIDEBOOK.md** — full official guidebook adaptation
- **GUIDEBOOK-SUMMARY.md** — one-page condensed reference
- **BACKEND.md** — server / web-play planning notes

*Official Guidebook: https://nethack.org/v367/Guidebook.html*
*Local copy: /usr/share/doc/nethack-common/Guidebook.txt.gz*

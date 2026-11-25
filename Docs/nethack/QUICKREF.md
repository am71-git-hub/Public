# NetHack Quick Reference

> Default keys (`number_pad:0`, vi movement). Smaller: [CHEATSHEET.txt](CHEATSHEET.txt). Deeper: [TUTORIAL-FULL.md](TUTORIAL-FULL.md).

## Movement

```
 y  k  u     hjkl + yubn       move (into monster = attack, into door = open)
  \ | /      H J K L Y U B N   run until something interesting
 h--.--l     G + dir           run, ignore corridor forks
  / | \      _                 travel to a chosen known tile
 b  j  n     m + dir           move without fighting / picking up
             F + dir           force attack
 . = wait    number first      repeat count:  10s  20.
```

No diagonal moves through doorways. Kick is `^D`, **not** `k`.

## Look / Info

| Key | Action | Key | Action |
|-----|--------|-----|--------|
| `:` | what's under me | `;` | examine any tile (cursor + `.`) |
| `/` | what is this glyph | `^P` | replay messages |
| `^X` | my stats | `^O` | dungeon overview |
| `\` | discovered items | `&` | what does this key do |
| `?` | help menu | `V` | game history |

## Inventory & Equipment

| Key | Action | Key | Action |
|-----|--------|-----|--------|
| `i` | inventory | `,` | pick up |
| `d` / `D` | drop / drop multi | `@` | toggle autopickup |
| `w` | wield weapon (`w-` = bare) | `x` | swap primary/secondary |
| `W` / `T` | wear / take off armor | `A` | remove all worn |
| `P` / `R` | put on / remove ring, amulet | `p` | pay shopkeeper |

Show worn/wielded: `)` weapon `[` armor `=` rings `"` amulet `(` tools `*` all.

## Using Items

| Key | Action | Key | Action |
|-----|--------|-----|--------|
| `e` | eat | `q` | quaff potion |
| `r` | read scroll/book | `z` | zap wand |
| `a` | apply tool | `E` | engrave (`E-` = in dust) |
| `t` | throw | `f` | fire from quiver (`Q` sets it) |
| `Z` | cast spell | `+` | list known spells |

## Dungeon

| Key | Action | Key | Action |
|-----|--------|-----|--------|
| `s` | search (use `10s`) | `^D` | kick (doors, chests) |
| `o` / `c` | open / close door | `^` | name trap under cursor |
| `>` / `<` | stairs down / up | `^T` | teleport (if able) |

## Extended Commands (`#` + name, autocompletes)

```
#pray     divine rescue — real trouble only, ~once / 1000 turns
#offer    sacrifice fresh corpse on altar
#chat     talk to adjacent creature
#loot     open container on floor       #tip      dump container out
#force    pry lock with weapon          #untrap   disarm a trap
#enhance  spend weapon/spell skill      #twoweapon  dual wield (also X)
#dip      dip object into potion        #rub      lamp / touchstone
#name     name item or monster type     #adjust   reassign inventory letter
#annotate note on this level            #overview level notes (also ^O)
```

## Meta

`S` save & quit (resume on relaunch) · `O` options · `^R` redraw · `#quit` abandon game

## Status Line Legend

```
Dlvl:1  $:0  HP:16(16)  Pw:2(2)  AC:6  Xp:1  T:42  Hungry
 depth  gold  hit points  energy   armor  level  turns  condition
                                   (lower=better)
```

Hunger: `Satiated → (ok) → Hungry → Weak → Fainting → Starved`. Eat at Hungry.
Bad conditions: `Conf` confused · `Stun` stunned · `Blind` · `Hallu` · `Ill` (pray!) · `FoodPois` (pray!)

## Symbol Legend

```
ITEMS   ) weapon  [ armor  ! potion  ? scroll  / wand  = ring  " amulet
        % food  ( tool  + spellbook/door  * gem  $ gold
MAP     . floor  # corridor  | - wall  + door  > < stairs  ^ trap
        { fountain  _ altar  \ throne  ` boulder
BEINGS  @ you/human  a-zA-Z monsters  d f your pet (dog/cat)  I unseen
```

## Emergencies

| Problem | Response |
|---------|----------|
| HP critical | `#pray`, or quaff unknown potions as a last resort |
| Food poisoning / Ill | `#pray` immediately — fatal in ~10–25 turns |
| Cursed item stuck | scroll of remove curse, holy water, or `#pray` |
| Surrounded | Elbereth: `E` `-` then type `Elbereth` — most monsters flee |
| Starving | `#pray`, eat anything non-poisonous |

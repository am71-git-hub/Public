# NetHack: learn to play

Beginner-friendly guides for [NetHack](https://www.nethack.org/) 3.6, the classic free dungeon game played in a terminal.
Every guide uses the **default keys** (vi-style movement, `number_pad:0`) unless it says otherwise.

## Start here

| Read | When |
|---|---|
| 1. [TUTORIAL.md](TUTORIAL.md) | Your first game: the screen, moving, fighting, eating, staying alive |
| 2. [QUICKREF.md](QUICKREF.md) | One-page key reference to keep open while you play |
| 3. [CHEATSHEET.txt](CHEATSHEET.txt) | Tiny crib sheet, fits beside the terminal |
| 4. [GUIDEBOOK-SUMMARY.md](GUIDEBOOK-SUMMARY.md) | The official Guidebook, condensed |
| 5. [TUTORIAL-FULL.md](TUTORIAL-FULL.md) | The complete tutorial: every command, monster class, item, strategy and option |
| 6. [GUIDEBOOK.md](GUIDEBOOK.md) | The official Guidebook, adapted to Markdown |
| ⚙ [BACKEND.md](BACKEND.md) | Config options, save files, and playing from a web browser through your own server |

## Install and play

| System | Install | Start |
|---|---|---|
| Debian / Ubuntu | `sudo apt install nethack-console` | `nethack-console` (or `/usr/games/nethack`) |
| Fedora | `sudo dnf install nethack` | `nethack` |
| Arch | `sudo pacman -S nethack` | `nethack` |
| macOS | `brew install nethack` | `nethack` |
| Windows | Download from [nethack.org](https://www.nethack.org/) | `NetHack.exe` |
| No install | Play in your browser at [nethack.alt.org](https://alt.org/nethack/) (via SSH or its web client) | |

## Use the ready-made configs

Two config files are included:

| File | For |
|---|---|
| [`nethackrc-laptop`](nethackrc-laptop) | Laptops / no numpad: vi keys `h j k l y u b n` |
| [`nethackrc-numpad`](nethackrc-numpad) | Full keyboards: numpad `1–9` moves, `5` waits |

Either run the game with one of them (Linux / macOS):

```bash
./play.sh            # laptop layout (default)
./play.sh numpad     # numpad layout
```

or make one your permanent default:

```bash
cp nethackrc-laptop ~/.nethackrc
```

## Credits

NetHack is © the NetHack DevTeam and is free software under the
[NetHack General Public License](https://www.nethack.org/common/license.html).
[GUIDEBOOK.md](GUIDEBOOK.md) and [GUIDEBOOK-SUMMARY.md](GUIDEBOOK-SUMMARY.md) are adapted from the
[official NetHack 3.6.7 Guidebook](https://www.nethack.org/v367/Guidebook.html) and keep its licence.
The other guides are original, under the same terms as the rest of this repository.

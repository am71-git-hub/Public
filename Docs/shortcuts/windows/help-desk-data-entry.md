# Help Desk Data Entry — Keyboard-First Cheat Sheet

For help desk and service desk work: **ServiceDesk Plus (SDP)**, **Teams**, **Outlook**, and a pile of web apps, all on Windows.
Most of it applies to any ticketing system or data-entry job.
The work is mostly *read → find the bit you need → copy → paste it somewhere else → type a note*.
Every section below is aimed at doing that loop without reaching for the mouse.

Last updated: 2026-11-23

---

## The 15 to learn first

Learn these before anything else. They cover about 80% of a data-entry day.

| Keys | What it does | Why it matters for you |
|---|---|---|
| `Ctrl + Shift + →` / `←` | Select the next / previous **word** | Grab a name, ticket #, or email word-by-word |
| `Shift + End` / `Shift + Home` | Select to the **end / start of the line** | Grab "the rest of this line" in one move |
| `Home`, then `Shift + End` | Select the **whole line** | Copy a full line of a ticket |
| `Ctrl + Backspace` / `Ctrl + Delete` | Delete the word **before / after** the cursor | Fix typos without holding Backspace |
| `Win + V` | **Clipboard history** (last 25 copies) | Copy 5 things, then paste them one by one |
| `Ctrl + Shift + V` | Paste as **plain text** (browsers, Teams, Office 365) | No weird fonts/colours when pasting into SDP |
| `Alt + Tab` | Switch window | SDP ↔ Teams ↔ Outlook |
| `Win + 1` … `Win + 9` | Open / jump to pinned taskbar app #1–9 | One key per app, no hunting |
| `Ctrl + Tab` / `Ctrl + Shift + Tab` | Next / previous browser tab | Move between tickets |
| `Ctrl + L` | Jump to the browser address bar | Type a URL, or `sdp 12345` to open a ticket |
| `Alt + ←` / `Alt + →` | Browser back / forward | Back to the ticket list |
| `Tab` / `Shift + Tab` | Next / previous form field | Move through SDP fields without clicking |
| `Ctrl + F` | Find on page | Find the serial number in a long ticket |
| `Ctrl + Z` | Undo | Fearless editing |
| `Win + L` | Lock the PC | Every time you stand up. You're the help desk. |

---

## Mouse moves that still save time

Clicking to select is fast when you know the tricks. Combine them with the keyboard.

| Action | Result |
|---|---|
| **Double-click** a word | Selects the word |
| **Triple-click** | Selects the whole line / paragraph (in a one-line box: everything) |
| Double-click, **keep holding and drag** | Extends the selection a *whole word* at a time |
| Triple-click, **keep holding and drag** | Extends by whole paragraphs |
| Click once, then **Shift + click** somewhere else | Selects everything between the two clicks |
| Select something, then **Shift + ← / →** | Fine-tune the selection one character at a time |
| Select something, then **Ctrl + Shift + ← / →** | Grow/shrink it one word at a time |
| **Ctrl + click** a link | Open it in a new background tab (stay where you are) |
| **Middle-click** a link | Same as Ctrl + click |
| **Middle-click** a browser tab | Close that tab |

**The combo to practise:** double-click the first word you want → `Ctrl + Shift + →` until you have it all → `Ctrl + C`.
That beats dragging and missing the last letter every time.

---

## Selecting text precisely (keyboard)

Cursor is in a text box (ticket notes, description, a reply).

| Keys | Moves / selects |
|---|---|
| `Ctrl + ←` / `Ctrl + →` | Jump one word left / right |
| `Home` / `End` | Start / end of line |
| `Ctrl + Home` / `Ctrl + End` | Start / end of the whole box or document |
| `Shift` + any of the above | Same jump, but **selects** as it goes |
| `Ctrl + Shift + ←` | Select the word **before** the cursor |
| `Ctrl + Shift + →` | Select the word **after** the cursor |
| `Shift + ↑` / `Shift + ↓` | Select up / down a line |
| `Ctrl + A` | Select everything in the box (in a box) or page (outside one) |

### Recipes

| You want to… | Do this |
|---|---|
| Copy the whole current line | `Home`, `Shift + End`, `Ctrl + C` |
| Copy from here to end of line | `Shift + End`, `Ctrl + C` |
| Copy the word you're in the middle of | `Ctrl + ←`, `Ctrl + Shift + →`, `Ctrl + C` |
| Delete the last word you typed | `Ctrl + Backspace` |
| Replace an entire field's contents | Click/Tab into it, `Ctrl + A`, just start typing |
| Copy a line and paste it below | `Home`, `Shift + End`, `Ctrl + C`, `End`, `Enter`, `Ctrl + V` |

### Selecting text on a web page that isn't in a box

Read-only ticket text can't be selected with arrows… unless you turn on **caret browsing**:

- Press **`F7`** in Chrome or Edge (it asks once to confirm).
- Now there's a blinking cursor on the page. Click near the text, then use `Shift + arrows`, `Ctrl + Shift + →`, `Shift + End` exactly like in a text box.
- Press `F7` again to turn it off.

---

## Copy / paste like a pro

| Keys | What it does |
|---|---|
| `Ctrl + C` / `Ctrl + X` / `Ctrl + V` | Copy / cut / paste |
| `Ctrl + Shift + V` | Paste **without formatting** (Chrome, Edge, Teams, current Office) |
| `Win + V` | Clipboard history — arrow to an item, `Enter` to paste it |
| `Win + V`, then **pin** an item | Keeps it forever (your email signature, a standard reply, the KB link you paste 30×/day) |
| `Win + Shift + S` | Screenshot a region → it's on the clipboard, paste straight into Teams/SDP |
| `Win + Shift + T` | (PowerToys Text Extractor) copy text *out of an image or screenshot* |

**First time:** press `Win + V` and click **Turn on**. Clipboard history is off by default.

**Multi-copy workflow** (e.g. moving user details from an email into an SDP ticket):
1. In the email, copy name → copy phone → copy asset tag → copy description (4 separate `Ctrl + C`s).
2. Go to SDP (`Alt + Tab`).
3. In each field: `Win + V`, arrow to the right item, `Enter`, then `Tab` to the next field.

---

## ServiceDesk Plus (SDP)

SDP is a web app, so **all the browser shortcuts work in it**. SDP itself has very few documented keyboard shortcuts (check *Help* in your version; ManageEngine changes the UI between releases). The big wins come from the browser and from SDP features:

### Jump straight to a ticket by number — set this up once

Make the address bar understand `sdp 12345`:

1. Open any ticket in SDP and copy its URL from the address bar.
2. Chrome: `Settings → Search engine → Manage search engines and site search → Site search → Add`.
   Edge: `Settings → Privacy, search, and services → Address bar and search → Manage search engines → Add`.
3. Name: `SDP` · Shortcut: `sdp` · URL: paste the ticket URL, then **replace the ticket number with `%s`**.
4. Now: `Ctrl + L`, type `sdp`, `Space` (or `Tab`), type the ticket number, `Enter`.

Do the same for anything else you look up by ID (user directory, asset system, KB articles).

### Moving around SDP forms

| Keys | In an SDP form |
|---|---|
| `Tab` / `Shift + Tab` | Next / previous field |
| Start typing in a focused dropdown | Filters the list (requester, category, technician) |
| `↑` / `↓`, then `Enter` | Pick from the filtered dropdown list |
| `Alt + ↓` | Open a standard dropdown without the mouse |
| `Space` | Tick / untick a focused checkbox |
| `Esc` | Close a popup or dropdown |
| `Ctrl + F` | Find text in a long ticket / conversation |
| `Ctrl + Enter` | Submits in some web text boxes — **test on a dummy ticket before relying on it** |

### Ticket list

| Action | How |
|---|---|
| Open several tickets without losing the list | `Ctrl + click` (or middle-click) each subject → they open in background tabs |
| Then work through them | `Ctrl + Tab` to the next one, `Ctrl + W` to close when done |
| Bookmark your common views | Filter the list the way you like (e.g. "My open"), `Ctrl + D` to bookmark it |
| Refresh the queue | `F5` |

### Use SDP's own time-savers

- **Reply / resolution templates** (sometimes called canned responses): saved text you insert instead of typing.
- **Request templates**: pre-filled forms for common ticket types (password reset, new hire, etc.).
- Ask your admin which exist — if you type the same paragraph more than twice a day, it should be a template (or a text-expansion snippet, see [power-tools.md](power-tools.md)).

---

## Teams (quick list — full sheet in [teams.md](teams.md))

| Keys | What it does |
|---|---|
| `Ctrl + .` | Show all Teams shortcuts |
| `Ctrl + E` | Jump to the search box |
| `Ctrl + N` | New chat |
| `Shift + Enter` | New line *without* sending |
| `Ctrl + Shift + X` | Expand the compose box (then `Enter` = new line) |
| `Ctrl + Shift + M` | Mute / unmute in a call |
| `Ctrl + Shift + E` | Share screen |

---

## Outlook (quick list — full sheet in [office.md](office.md))

| Keys | What it does |
|---|---|
| `Ctrl + R` / `Ctrl + Shift + R` | Reply / reply all |
| `Ctrl + F` | **Forward** (not find! Search is `Ctrl + E`) |
| `Ctrl + Q` / `Ctrl + U` | Mark read / unread |
| `Ctrl + Shift + V` | Move to folder |
| `Ctrl + Shift + M` | New email from anywhere in Outlook |
| `Alt + S` | Send |

---

## Windows & window juggling (full sheet in [windows-desktop.md](windows-desktop.md))

| Keys | What it does |
|---|---|
| `Win + ←` / `Win + →` | Snap window to left / right half (reading on one side, typing on the other) |
| `Win + ↑` | Maximise |
| `Win + Shift + ←/→` | Move window to the other monitor |
| `Win + D` | Show desktop / bring everything back |
| `Win + Ctrl + D` / `Win + Ctrl + ←/→` | New virtual desktop / switch desktops |
| `Ctrl + Shift + Esc` | Task Manager (when something freezes) |
| `Win + R` | Run box — see help-desk commands in [windows-desktop.md](windows-desktop.md) |

**Recommended layout:** pin your apps to the taskbar in this order and the numbers become muscle memory:
`Win+1` browser (SDP) · `Win+2` Teams · `Win+3` Outlook · `Win+4` Excel/whatever's next.

---

## A 4-week practice plan

Don't try to learn it all at once. Pick a few, force yourself to use them, add more when they feel automatic.

| Week | Focus | Rule for the week |
|---|---|---|
| 1 | `Ctrl+Shift+←/→`, `Shift+Home/End`, `Ctrl+Backspace`, double/triple-click + `Shift+click` | No drag-selecting text with the mouse |
| 2 | `Win+V` (pin 3 things), `Ctrl+Shift+V`, `Win+1…9`, `Alt+Tab` | No clicking the taskbar |
| 3 | Browser: `Ctrl+L`, `Ctrl+Tab`, `Ctrl+W`, `Ctrl+click`, the `sdp` site-search shortcut | No clicking browser tabs |
| 4 | `Tab` through SDP forms, Teams/Outlook keys, snap windows | No touching the mouse for one full ticket, start to finish |

**Tip:** print the "15 to learn first" table and tape it under your monitor. When you catch yourself reaching for the mouse, stop and look it up — that's how they stick.

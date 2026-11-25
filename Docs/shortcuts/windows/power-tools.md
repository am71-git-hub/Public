# Power Tools — Going Beyond Built-in Shortcuts

Once the built-in shortcuts are automatic, these tools let you make your *own*.

> **Work PC:** you're IT, but still ask before installing anything — most of these need admin rights
> or approval. Built-in options are listed first.

---

## Built in — no install needed

| Tool | How | Use |
|---|---|---|
| **Clipboard history** | `Win + V` → Turn on | Last 25 copies; **pin** your most-pasted text |
| **Snipping Tool** | `Win + Shift + S` | Region screenshot to clipboard |
| **Text from screenshots** | Snipping Tool → *Text actions* (Win 11) | Copy text out of an image someone sent |
| **Sticky Keys** etc. | Know how to turn *off* if a user triggers it (press `Shift` 5×) | |
| **Custom app hotkeys** | Right-click a Start/desktop shortcut → Properties → *Shortcut key* | e.g. `Ctrl + Alt + S` opens SDP |
| **Browser site search** | See [browser-chrome-edge.md](browser-chrome-edge.md) | `sdp 12345` jumps to a ticket |

## Microsoft PowerToys (free, from Microsoft)

| Feature | Default key | Use |
|---|---|---|
| **PowerToys Run / Command Palette** | `Alt + Space` (Run) / `Win + Alt + Space` (Command Palette) | Launcher: apps, files, calculator, web search |
| **Text Extractor** | `Win + Shift + T` | Drag over any screen area → its text is copied (OCR) |
| **Advanced Paste** | `Win + Shift + V` (menu), `Win + Ctrl + Alt + V` (plain text) | Paste as plain text / other formats anywhere |
| **FancyZones** | `` Win + Shift + ` `` (editor), hold `Shift` while dragging | Custom window layouts for wide monitors |
| **Keyboard Manager** | settings | Remap keys (e.g. Caps Lock → Ctrl or Esc) |
| **Shortcut Guide** | hold `Win` | Shows Win-key shortcuts on screen |
| **Always on Top** | `Win + Ctrl + T` | Pin the ticket you're copying *from* above everything |
| **Find My Mouse** | double-tap left `Ctrl` | Find the cursor on multiple screens |

(Defaults change between versions — check each feature's settings page.)

## Text expansion — stop typing the same notes

You type the same phrases all day: greetings, "please restart and try again", resolution notes.
A text expander turns a short code into the full text.

| Option | Notes |
|---|---|
| **SDP reply/resolution templates** | Built into SDP — ask your admin. Best first choice. |
| **Outlook Quick Parts / My Templates** | For email only |
| **AutoHotkey** (free) | Works everywhere; needs install approval |
| **Espanso** (free, open source) | Cross-platform (Windows + Linux), simple config file |

AutoHotkey v2 example (`hotstrings.ahk`):

```ahk
; type ;pw then space/enter -> expands
::;pw::Password reset completed. User confirmed they can sign in.
::;rst::Please restart your computer and let me know if the issue continues.
::;ty::Thanks for contacting the Help Desk!
::;sig::Your Name`nIT Help Desk

; Ctrl+Alt+D types today's date
^!d::Send FormatTime(, "yyyy-MM-dd")
```

Start each code with `;` so you never trigger one by accident.

## Browser extensions (ask first)

| Extension | Use |
|---|---|
| **Vimium** / **Vimium C** | Press `f` and every link/button gets a letter label — click anything from the keyboard |
| **Text Blaze** / **Magical** | Text expansion inside the browser, with fill-in fields |
| **Shortkeys** | Bind your own keys to browser actions |

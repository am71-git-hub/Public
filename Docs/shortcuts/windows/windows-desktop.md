# Windows Desktop — Windows 10 / 11

Window management, the Win key, dialog boxes, File Explorer, and Run commands a help desk tech should know.

---

## Switching apps & windows

| Keys | Action |
|---|---|
| `Alt + Tab` | Switch window (hold `Alt`, tap `Tab` to go further) |
| `Alt + Shift + Tab` | Switch backwards |
| `Ctrl + Alt + Tab` | Sticky switcher — stays open, pick with arrows + `Enter` |
| `Win + Tab` | Task View (all windows + virtual desktops) |
| `Win + 1…9` | Open / switch to pinned taskbar app #n (press again to cycle its windows) |
| `Win + Shift + 1…9` | Open a **new** window of app #n |
| `Win + Alt + 1…9` | Jump list (recent files) for app #n |
| `Win + T` | Cycle through taskbar icons (`Enter` to open) |
| `Alt + Esc` | Cycle windows in the order they were opened |

## Arranging windows

| Keys | Action |
|---|---|
| `Win + ←` / `→` | Snap to left / right half |
| `Win + ↑` | Maximise (or snap to top half after a side snap) |
| `Win + ↓` | Restore / minimise |
| `Win + Z` | Snap layouts menu (Windows 11) |
| `Win + Shift + ←/→` | Move window to the other monitor |
| `Win + Home` | Minimise everything except the active window |
| `Win + D` | Show desktop (press again to restore) |
| `Win + M` / `Win + Shift + M` | Minimise all / restore |
| `Alt + Space` | Window menu (then `N` minimise, `X` maximise, `M` move with arrows) |
| `Alt + F4` | Close window (on the desktop: shut down dialog) |

## Virtual desktops

| Keys | Action |
|---|---|
| `Win + Ctrl + D` | New desktop |
| `Win + Ctrl + ←/→` | Switch desktop |
| `Win + Ctrl + F4` | Close current desktop |

Idea: desktop 1 = tickets & Teams, desktop 2 = admin tools / remote sessions.

## The Win key

| Keys | Opens |
|---|---|
| `Win` then type | Search / launch anything (apps, settings, files) |
| `Win + E` | File Explorer |
| `Win + R` | Run box |
| `Win + I` | Settings |
| `Win + X` | Power-user menu (Device Manager, Terminal, Disk Mgmt… — letters jump) |
| `Win + L` | **Lock** |
| `Win + V` | Clipboard history |
| `Win + Shift + S` | Snip a region to clipboard |
| `Win + PrtScn` | Full screenshot saved to Pictures\Screenshots |
| `Win + .` | Emoji & symbols panel |
| `Win + H` | Voice typing |
| `Win + A` | Quick settings (Wi-Fi, volume…) |
| `Win + N` | Notifications / calendar |
| `Win + Ctrl + Enter` | Narrator on/off (know this in case a user turns it on by accident) |
| `Win + +` / `Win + Esc` | Magnifier on / off (same) |
| `Win + Ctrl + Shift + B` | Restart the graphics driver (black/frozen screen fix) |
| `Ctrl + Shift + Esc` | Task Manager directly |
| `Ctrl + Alt + Del` | Security screen (lock, switch user, Task Manager) |

## Dialog boxes & forms (old-style Windows apps)

| Keys | Action |
|---|---|
| `Tab` / `Shift + Tab` | Next / previous control |
| `Enter` | Default button (usually OK) |
| `Esc` | Cancel |
| `Space` | Press focused button / toggle checkbox |
| `Alt + underlined letter` | Jump to that control (press `Alt` to reveal underlines) |
| Arrow keys | Move within a radio group or list |
| `Alt + ↓` or `F4` | Open a dropdown |
| Type letters | Jump to matching item in a list |
| `Ctrl + Tab` / `Ctrl + Shift + Tab` | Next / previous tab in a tabbed dialog |

## File Explorer

| Keys | Action |
|---|---|
| `Alt + D` or `Ctrl + L` | Address bar (type a path like `\\server\share` or `%appdata%`) |
| `Alt + ↑` | Up one folder |
| `Alt + ←` / `→` | Back / forward |
| `Ctrl + E` or `Ctrl + F` | Search box |
| `F2` | Rename |
| `Ctrl + Shift + N` | New folder |
| `Alt + Enter` | Properties |
| `Ctrl + Shift + C` (Win 11) | Copy the file's full path |
| `Shift + right-click` | Extended menu incl. "Copy as path" (Win 10) |
| `Ctrl + mouse wheel` | Change icon size / view |
| `Shift + Delete` | Delete permanently (no Recycle Bin) |

## Run box commands (`Win + R`) — help desk favourites

| Type | Opens |
|---|---|
| `cmd` / `powershell` | Command prompt / PowerShell (`Ctrl + Shift + Enter` = run as admin) |
| `control` | Control Panel |
| `appwiz.cpl` | Programs and Features (uninstall) |
| `ncpa.cpl` | Network adapters |
| `devmgmt.msc` | Device Manager |
| `services.msc` | Services |
| `eventvwr` | Event Viewer |
| `compmgmt.msc` | Computer Management |
| `diskmgmt.msc` | Disk Management |
| `lusrmgr.msc` | Local users & groups |
| `printmanagement.msc` | Print Management (Pro/Enterprise) |
| `dsa.msc` | Active Directory Users & Computers (if RSAT installed) |
| `mstsc` | Remote Desktop |
| `msinfo32` | System info (model, serial-ish, RAM, BIOS) |
| `winver` | Windows version / build |
| `taskmgr` | Task Manager |
| `%temp%` | Temp folder |
| `\\computername\c$` | Admin share on a remote PC (with rights) |

Most of these also work typed straight into the Start menu after pressing `Win`.

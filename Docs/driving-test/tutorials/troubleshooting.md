# Troubleshooting

[← Back to the G1 study kit](../README.md)

---

## Opening the file

| Problem | Fix |
|---|---|
| It opens as a page of code in Notepad / TextEdit | Right-click the file → **Open with** → your browser (Chrome, Edge, Safari, Firefox). |
| Blank page | Make sure JavaScript isn't turned off in your browser. Try another browser. |
| Downloaded file is tiny (a few KB) or shows GitHub's web page | You saved the GitHub page, not the file. Use the **Download raw file** button ([tutorial 1](01-open-the-file.md)). |
| Opens as text on a phone | The file app used a basic viewer. Open it from a web address instead ([tutorial 3](03-phones-and-tablets.md)). |

## Progress

| Problem | Fix |
|---|---|
| My progress disappeared | Progress belongs to **one browser on one device**, tied to the file or address. A different browser, a moved/renamed file, a different address (`localhost` vs the IP address), a private window, or clearing browsing data each start fresh. |
| I want it on two devices | Progress can't be copied between devices; each one keeps its own. |
| Nothing is being saved | You may be in **no-save mode** (the home screen says 🕶 No-save mode), or in a private window. |
| Start over | **⚙️ Text size and read aloud** → **🗑 Reset my progress** |

## Read aloud

| Problem | Fix |
|---|---|
| "This browser has no built-in voice" | Try Chrome, Edge or Safari. Some Linux browsers have no voices installed (on Linux, install `speech-dispatcher` and `espeak-ng`, then restart the browser). |
| Robotic voice | Pick another voice in **⚙️** settings. Windows: **Settings → Time & language → Speech** to add voices. Android: **Settings → Accessibility → Text-to-speech**. iPhone: **Settings → Accessibility → Spoken Content → Voices**. |
| No sound | Check the device volume and silent switch. On phones, media volume is separate from ringer volume. |

## Web server ([tutorials 4](04-share-on-your-wifi.md) and [5](05-run-it-all-the-time.md))

| Problem | Fix |
|---|---|
| `python3` / `py` not found | Install Python ([tutorial 4, step 1](04-share-on-your-wifi.md#step-1-get-python-3)). On Windows, re-run the installer and tick **Add python.exe to PATH**. |
| `Address already in use` | Something else uses port 8095, maybe an earlier server still running. Close it, or use another port such as `8096`. |
| `No such file or directory: 'site'` | Run the command from **inside** the `driving-test` folder. |
| Works on the computer, not on the phone | Same Wi-Fi? Correct IP address? On Windows, allow Python through the firewall for **Private networks**. On Linux, if you used the service file, remove `--bind 127.0.0.1`. Guest Wi-Fi networks often block devices from seeing each other. |
| Linux service won't start | `journalctl --user -u driving-test -n 30` shows why. Usually the path after `--directory` is wrong. |

## Rebuilding ([tutorial 7](07-edit-and-rebuild.md))

| Problem | Fix |
|---|---|
| `missing picture img/…` | The `img` path in the question doesn't match a file in `img/`. Paths are case-sensitive. |
| `needs exactly 3 wrong answers` | `w` must list exactly three wrong answers. |
| `choices are not all different` | Two answers are identical; reword one. |
| JSON error | A missing comma or quote. Paste the file into a JSON validator to find the line. |

Still stuck? Open an issue on GitHub and describe what you tried.

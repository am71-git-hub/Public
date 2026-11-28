# 8 · Shut down and clean up

[← Back to the G1 study kit](../README.md)

Passed your test? This page undoes everything the other tutorials set up, so nothing is left running
and nothing is left saved. Do only the sections for the things you actually did.

| You did… | Undo it with |
|---|---|
| Started the server by hand ([tutorial 4](04-share-on-your-wifi.md)) | [Stop a hand-started server](#stop-a-hand-started-server) |
| Made it start automatically ([tutorial 5](05-run-it-all-the-time.md)) | [Remove the auto-start](#remove-the-auto-start) |
| Used the app in a browser | [Clear saved progress](#clear-saved-progress) |
| Added a home-screen icon ([tutorial 3](03-phones-and-tablets.md)) | [Remove the icon](#remove-the-home-screen-icon) |
| Downloaded the files | [Delete or keep the files](#delete-or-keep-the-files) |

---

## Stop a hand-started server

Go to the terminal window that says `Serving HTTP on … port 8095` and press `Ctrl + C`, or close the window.
It won't start again unless you run the command again.

## Remove the auto-start

### Linux (systemd user service)

```bash
systemctl --user disable --now driving-test        # stop it and turn off start-at-boot
rm ~/.config/systemd/user/driving-test.service     # delete the service file
systemctl --user daemon-reload                     # make systemd forget it
systemctl --user reset-failed driving-test         # clear any leftover state (no output is fine)
```

**Did you turn on lingering** (`loginctl enable-linger`, step 5 of tutorial 5)? Turn it back off **only if
nothing else of yours needs it**. Check first with `systemctl --user list-unit-files --state=enabled`;
if the list is empty:

```bash
loginctl disable-linger "$USER"
```

### Windows (Startup folder)

1. Close the **G1 practice server** window if it's open.
2. Press `Win + R`, type `shell:startup`, press Enter.
3. Delete `g1-practice.bat`.

### Mac (launchd)

```bash
launchctl unload ~/Library/LaunchAgents/local.g1-practice.plist
rm ~/Library/LaunchAgents/local.g1-practice.plist
```

### Firewall (Windows)

If you clicked **Allow** when Windows asked about the firewall, remove that rule:
**Windows Security → Firewall & network protection → Allow an app through firewall → Change settings**,
find **Python**, and untick it (or click **Remove**). Skip this if you use Python for anything else.

## Check it's really off

| Computer | Run | You want |
|---|---|---|
| **Linux** | `systemctl --user status driving-test` then `ss -ltn \| grep 8095` | "could not be found", then no output |
| **Mac** | `lsof -i :8095` | no output |
| **Windows** | `netstat -ano \| findstr :8095` | no output |

Or simply open **http://localhost:8095**: you should get "This site can't be reached".

## Clear saved progress

The app saves scores, missed questions and settings in your browser, **separately for each address you
opened it from** (the GitHub link, `localhost:8095`, `192.168.x.x:8095`, or a downloaded file).
Nothing was ever sent anywhere, so this only matters on shared devices or if you want a clean slate.

**Quickest:** in the app, open **Settings** and use **Reset my progress** on each device and address you used.

**From the browser instead:**

| Browser | Steps |
|---|---|
| **Chrome / Edge** | Settings → Privacy and security → Site settings → **View permissions and data stored across sites** → search the address (e.g. `localhost` or `am71-git-hub.github.io`) → delete |
| **Firefox** | Settings → Privacy & Security → Cookies and Site Data → **Manage Data** → search the address → Remove |
| **Safari (Mac)** | Settings → Privacy → **Manage Website Data** → search → Remove |
| **iPhone / iPad** | Settings → Safari → Advanced → **Website Data** → search → swipe to delete |

Used the **no-save version**? There's nothing to clear.

## Remove the home-screen icon

- **Android:** long-press the icon → **Remove** (or drag it to **Remove**).
- **iPhone / iPad:** long-press the icon → **Remove App** → **Delete from Home Screen**.

## Delete or keep the files

The app is just files, so deleting the folder removes it completely. Delete the downloaded ZIP and the
unzipped `driving-test` folder (or the whole `Public` folder if you cloned the repository).

Thinking of keeping it for a friend or family member? The single file `site/index.html` is the whole app.
Keep that one file and you can always open it again, or share it, with no server at all.

## Bring it back later

Start again from [tutorial 1](01-open-the-file.md), or just open the
[online version](https://am71-git-hub.github.io/Public/Docs/driving-test/site/).

# 5 · Run it all the time

[← Back to the G1 study kit](../README.md)

[Tutorial 4](04-share-on-your-wifi.md) starts the server by hand. This page makes it **start automatically**
whenever the computer starts, so the app is always there for every device in the house.

In every example, replace the folder path with where **your** copy of `driving-test/site` is.

---

## Linux (systemd user service)

The repository includes a ready-made service file: [`driving-test.service`](../driving-test.service).

1. **Copy it into place:**

   ```bash
   mkdir -p ~/.config/systemd/user
   cp driving-test.service ~/.config/systemd/user/
   ```

2. **Edit the path and options** in `~/.config/systemd/user/driving-test.service`:

   ```ini
   ExecStart=/usr/bin/python3 -m http.server 8095 --bind 127.0.0.1 --directory %h/Public/Docs/driving-test/site
   ```

   - `%h` means your home folder. Change `Public/Docs/driving-test/site` to your path.
   - `--bind 127.0.0.1` means **only this computer** can open it. **Delete** `--bind 127.0.0.1` to let phones and tablets on your Wi-Fi in.

3. **Start it, and turn on start-at-boot:**

   ```bash
   systemctl --user daemon-reload
   systemctl --user enable --now driving-test
   ```

4. **Check it:**

   ```bash
   systemctl --user status driving-test        # should say "active (running)"
   journalctl --user -u driving-test -f        # live log of page visits (Ctrl+C to stop watching)
   ```

5. **Keep it running when you're logged out** (optional, for an always-on computer):

   ```bash
   loginctl enable-linger "$USER"
   ```

| To… | Run |
|---|---|
| Restart (after editing the service file; a rebuild doesn't need one) | `systemctl --user daemon-reload && systemctl --user restart driving-test` |
| Stop | `systemctl --user stop driving-test` |
| Turn off start-at-boot | `systemctl --user disable --now driving-test` |

## Windows (Startup folder)

1. Press `Win + R`, type `shell:startup`, press Enter. The **Startup** folder opens.
2. Right-click in it → **New** → **Text Document**. Name it `g1-practice.bat` (say **Yes** to changing the extension).
3. Right-click it → **Edit**, and paste (with your own path):

   ```bat
   @echo off
   cd /d "C:\Users\YourName\Downloads\Public-main\Docs\driving-test"
   start "G1 practice server" /min py -m http.server 8095 --directory site
   ```

4. Save. Double-click it once to start now. From then on it starts minimised every time you sign in.

To stop it, close the **G1 practice server** window. To turn it off for good, delete the `.bat` file from the Startup folder.

## Mac (launchd)

1. Find Python's full path: run `which python3` in Terminal (for example `/usr/bin/python3` or `/opt/homebrew/bin/python3`).
2. Create `~/Library/LaunchAgents/local.g1-practice.plist` with this content (fix both paths):

   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
   <plist version="1.0">
   <dict>
     <key>Label</key><string>local.g1-practice</string>
     <key>ProgramArguments</key>
     <array>
       <string>/usr/bin/python3</string>
       <string>-m</string><string>http.server</string><string>8095</string>
       <string>--directory</string><string>/Users/yourname/Public/Docs/driving-test/site</string>
     </array>
     <key>RunAtLoad</key><true/>
     <key>KeepAlive</key><true/>
   </dict>
   </plist>
   ```

3. Load it:

   ```bash
   launchctl load ~/Library/LaunchAgents/local.g1-practice.plist
   ```

To stop it for good: `launchctl unload ~/Library/LaunchAgents/local.g1-practice.plist`, then delete the file.

## After it's running

Open **http://localhost:8095** on that computer, or **http://&lt;computer's IP&gt;:8095** on other devices
([how to find the IP](04-share-on-your-wifi.md#step-4-open-it-on-other-devices)).

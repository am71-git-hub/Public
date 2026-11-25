# 4 · Share it on your Wi-Fi

[← Back to the G1 study kit](../README.md)

Run a tiny web server on one computer, and every phone, tablet and laptop in the house can open the app
in a browser. It uses **Python**, which is free, and the server built into it. No setup files, no accounts.

---

## Step 1: Get Python 3

| Computer | Check | Install if missing |
|---|---|---|
| **Windows** | Open **Command Prompt**, type `py --version` | Install from [python.org](https://www.python.org/downloads/) (tick **Add python.exe to PATH**) or the Microsoft Store |
| **Mac** | Open **Terminal**, type `python3 --version` | macOS offers to install it the first time you run `python3`, or use [python.org](https://www.python.org/downloads/) |
| **Linux** | `python3 --version` | Almost always already installed. Otherwise `sudo apt install python3` (or your distro's equivalent) |

## Step 2: Start the server

You need the `driving-test/site` folder on your computer (download the ZIP, see [tutorial 1](01-open-the-file.md)).
Open a terminal **in the `driving-test` folder** and run:

**Windows (Command Prompt or PowerShell):**

```bat
py -m http.server 8095 --directory site
```

**Mac / Linux:**

```bash
python3 -m http.server 8095 --directory site
```

You'll see `Serving HTTP on :: port 8095 …`. Leave this window open: the server runs as long as it's open.

> **How to open a terminal in a folder.** Windows: open the folder in File Explorer, click the address bar, type `cmd`, press Enter.
> Mac: right-click the folder → **Services** → **New Terminal at Folder**. Linux: right-click → **Open in Terminal**.

## Step 3: Open it on the same computer

Go to **http://localhost:8095** in your browser. The app loads.

## Step 4: Open it on other devices

Find your computer's **local IP address**:

| Computer | How |
|---|---|
| **Windows** | In Command Prompt: `ipconfig` → look for **IPv4 Address**, e.g. `192.168.1.50` |
| **Mac** | `ipconfig getifaddr en0`, or **System Settings** → **Wi-Fi** → **Details** → IP address |
| **Linux** | `hostname -I` (the first address) |

On the phone or tablet, connected to the **same Wi-Fi**, open:

```
http://192.168.1.50:8095
```

(use your own address). Add `/?nosave` to the end for [no-save mode](02-no-save-mode.md).

**Windows asks about the firewall?** Choose **Allow** for **Private networks** only.

## Stop the server

Press `Ctrl + C` in the terminal window, or just close it.

## Good to know

- **It only shares the `site` folder**, nothing else on your computer.
- **Keep it on your home network.** Don't set up port forwarding on your router to put it on the internet.
  For access from anywhere, use free hosting instead ([tutorial 3, way C](03-phones-and-tablets.md#c-put-it-on-free-web-hosting-works-anywhere-any-device)),
  or a private VPN like Tailscale or WireGuard if you already use one.
- **Port 8095 already in use?** Pick another number, like `8096`, in both the command and the address.
- **The address changed?** Home routers sometimes hand out new addresses. Check again with the commands above,
  or give the computer a fixed address in your router's settings.
- Want it to start by itself every time the computer starts? → [Run it all the time](05-run-it-all-the-time.md)

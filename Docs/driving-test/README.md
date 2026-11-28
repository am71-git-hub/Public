# 🚗 Ontario G1 written test: free study kit

Everything you need to pass the **Ontario G1 knowledge test**, organized the same way the real test is: **Signs** and **Rules**.

- A **practice web app** in **one HTML file**: no install, no account, no internet needed once you have the file.
- **600+ practice questions**, each with the exact handbook words that prove the answer.
- **Study guides** for every topic, a numbers cheat sheet, flashcards and a **mock G1 test** marked like the real one.
- **Read aloud** on every question, so you can practise for the audio version of the test.

> Not made or endorsed by the Ontario government, the MTO or DriveTest. Built from the free
> [Official MTO Driver's Handbook](https://www.ontario.ca/document/official-mto-drivers-handbook). See [sources](sources.md).

---

## ▶ Use it now

**[Open the G1 practice app](https://am71-git-hub.github.io/Public/Docs/driving-test/site/)**: works on any phone, tablet or computer, nothing to install.
On a phone, add it to your home screen for a one-tap icon ([how](tutorials/03-phones-and-tablets.md#add-a-home-screen-icon)).

Prefer nothing saved? Use the **[no-save version](https://am71-git-hub.github.io/Public/Docs/driving-test/site/g1-practice-no-save.html)**.

Your progress stays on your device either way: the page is just served from GitHub, which never sees your answers.

## Or download it (works offline)

1. Open [`site/index.html`](site/index.html) here on GitHub and click **Download raw file** (the ⬇ button at the top right of the file view).
2. Double-click the downloaded file. It opens in your web browser.
3. That's it. Works on Windows, Mac, Linux and Chromebook, with or without Wi-Fi.

Your progress (scores, missed questions, settings) is saved **in that browser on that computer only**. Nothing is sent anywhere.

**Don't want anything saved?** Download [`site/g1-practice-no-save.html`](site/g1-practice-no-save.html) instead. Same app, but it forgets everything when you close the tab. Good for shared or public computers.

## Tutorials

| | Tutorial | For |
|---|---|---|
| 1 | [Open the file](tutorials/01-open-the-file.md) | Downloading and opening the app on any computer |
| 2 | [No-save mode](tutorials/02-no-save-mode.md) | Using it without leaving anything behind |
| 3 | [Phones and tablets](tutorials/03-phones-and-tablets.md) | Getting it onto Android, iPhone and iPad, plus a home-screen icon |
| 4 | [Share it on your Wi-Fi](tutorials/04-share-on-your-wifi.md) | Running a tiny web server so every device in the house can use it |
| 5 | [Run it all the time](tutorials/05-run-it-all-the-time.md) | Starting the server automatically (Linux, Windows, Mac) |
| 6 | [Using the app](tutorials/06-using-the-app.md) | What every screen does, and how to study with it |
| 7 | [Edit and rebuild](tutorials/07-edit-and-rebuild.md) | Changing questions or guides and rebuilding the page |
| 8 | [Shut down and clean up](tutorials/08-shut-down-and-clean-up.md) | Stopping the server, removing auto-start, clearing saved progress |
| ? | [Troubleshooting](tutorials/troubleshooting.md) | Voices, lost progress, blocked files, server problems |

## What's inside

| | |
|---|---|
| 📋 [Test day](test-day.md) | How the test works, what to bring, fees, and the **read-aloud (audio) option** |
| 🚸 [Signs half](signs/README.md) | 7 topics: every sign, light and road marking in the handbook, with pictures, plus **300 questions** |
| 📘 [Rules half](rules/README.md) | 13 topics, plus **300 questions** and the 8 official MTO sample questions |
| 🔢 [Every number in one place](rules/guide/R0-numbers.md) | Demerit points, distances, days and dollars, with memory tricks |
| 📚 [Sources](sources.md) | Where every fact comes from, and the rules that changed recently |

Everything in the app is also readable right here on GitHub as plain pages, so you can study without the app too.

## How the real test works

- **40 questions**: **20 signs + 20 rules**. You need **16/20 in each half**.
- The real MTO questions are secret, so these are written from the **Official MTO Driver's Handbook** in the same 4-choice style. The **8 official sample questions** from the handbook are included word for word (marked ⭐).

## 7-day study plan

| Day | Do this |
|---|---|
| 1 | Read [Test day](test-day.md). Signs **S1–S3** guides + practice. |
| 2 | Signs **S4–S7** + signs flashcards. Then 40 mixed sign questions. |
| 3 | Rules **R0 numbers**, **R1 licensing**, **R2 demerit points**, **R3 suspensions**. |
| 4 | Rules **R4–R8** (right-of-way, stopping, turns, sharing the road, speed). |
| 5 | Rules **R9–R13** (parking, freeways, weather and emergencies, safe driving, vehicle). |
| 6 | Mock test ×2. Then practice **Missed questions** until the list is empty. |
| 7 | Numbers flashcards. Mock test until you pass **3 in a row**. Rest. |

## How the files fit together

| Path | What it is |
|---|---|
| `site/index.html` | **The app.** One self-contained file (built, don't edit by hand). |
| `site/g1-practice-no-save.html` | The same app in no-save mode. |
| `data/signs.json` | Every sign: picture, name, handbook meaning. Builds the signs guides and flashcards. |
| `data/numbers.json` | Every number. Builds the numbers cheat sheet and the rules flashcards. |
| `data/questions/*.json` | The question bank, one file per topic. |
| `rules/guide/R1–R13*.md` | Hand-written rules study guides. |
| `app/` | The web page source (HTML template, CSS, JavaScript). |
| `build.py` | Checks everything and writes both HTML files plus the generated md files. |
| `driving-test.service` | Optional: keeps a local web server running on Linux ([tutorial 5](tutorials/05-run-it-all-the-time.md)). |
| `img/` | Pictures from the handbook (© King's Printer for Ontario, see [sources](sources.md)). |

## Privacy

The app makes **no network requests**: no tracking, no ads, no fonts or scripts loaded from the internet.
Read aloud uses your device's built-in voices. Saved progress lives only in your browser's local storage,
and the no-save version doesn't even use that.

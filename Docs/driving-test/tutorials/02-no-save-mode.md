# 2 · No-save mode

[← Back to the G1 study kit](../README.md)

Normally the app remembers your scores, missed questions and settings in your browser.
**No-save mode** turns that off completely: nothing is read from or written to the browser.
Close or reload the tab and it's all gone.

Use it on a **shared, library or work computer**, or when you just want a quick quiz with no history.

---

## Way 1: Use the no-save file

Download [`site/g1-practice-no-save.html`](../site/g1-practice-no-save.html) instead of `index.html`
(same steps as [tutorial 1](01-open-the-file.md)) and open it.

The home screen says **🕶 No-save mode** so you know it's on.

## Way 2: Add `?nosave` to the address

If you're opening the app from a web server ([tutorial 4](04-share-on-your-wifi.md)), add `?nosave`
to the end of the address:

```
http://localhost:8095/?nosave
http://192.168.1.50:8095/?nosave
```

Bookmark that address and it always opens in no-save mode.

## What's kept and what isn't

| | Normal | No-save |
|---|---|---|
| Progress while the tab is open | ✅ | ✅ |
| Missed-questions list during the session | ✅ | ✅ |
| Mock test scores | ✅ kept | ❌ gone when you close the tab |
| Text size and read-aloud settings | ✅ kept | ❌ back to default next time |
| Anything sent over the internet | ❌ never | ❌ never |

## Related

- A browser **private / incognito window** gives a similar result with the normal file:
  the browser throws away saved data when you close the window.
- To wipe saved progress in normal mode: **⚙️ Text size and read aloud** → **🗑 Reset my progress**.

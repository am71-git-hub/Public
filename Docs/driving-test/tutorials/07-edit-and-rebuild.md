# 7 · Edit and rebuild

[← Back to the G1 study kit](../README.md)

Everything in the app is generated from plain files. Change a file, run one command, and both HTML files
plus the study pages are rebuilt. Use this to fix a question, add your own, or update a rule that changed.

You need **Python 3** (standard library only, nothing to install) and a copy of the whole `driving-test` folder.

---

## Rebuild

From inside the `driving-test` folder:

```bash
python3 build.py          # Windows: py build.py
```

It checks every question and picture, then writes:

| Output | What |
|---|---|
| `site/index.html` | The app |
| `site/g1-practice-no-save.html` | The app in no-save mode |
| `signs/guide/S*.md`, `rules/guide/R0-numbers.md` | Generated study guides |
| `signs/questions/*.md`, `rules/questions/*.md` | Question pages (answers hidden until clicked) |
| `signs/README.md`, `rules/README.md` | Topic lists |

It ends with `0 problems.` If something's wrong it lists each problem (file and question number) and stops.

If you run a server ([tutorial 4](04-share-on-your-wifi.md)), just reload the page. With the Linux
service ([tutorial 5](05-run-it-all-the-time.md)) no restart is needed either: it serves the new file straight away.

## Where things live

| To change… | Edit |
|---|---|
| A question | `data/questions/<topic>.json` (e.g. `R2.json` = demerit points, `S2.json` = regulatory signs) |
| A rules study guide | `rules/guide/R1–R13*.md` (hand-written) |
| A sign's name or meaning | `data/signs.json` |
| A number (points, metres, fines) | `data/numbers.json` |
| Look and feel | `app/style.css` |
| How the app works | `app/app.js` (plain JavaScript, no frameworks) |

Don't edit the generated files listed above. They're overwritten on every build.

## Question format

Each topic file is a JSON list of questions:

```json
{
  "t": "numbers",
  "q": "How long do demerit points stay on your record?",
  "a": "2 years from the date of the offence",
  "w": ["1 year from the date of conviction", "3 years from the date of the offence", "5 years from the date of conviction"],
  "e": "2 years, counted from the offence date.",
  "s": "Demerit points stay on your record for two years from the date of the offence."
}
```

| Field | Meaning | Required |
|---|---|---|
| `t` | Question type (see below) | yes |
| `q` | The question | yes |
| `a` | The right answer | yes |
| `w` | Exactly **3** wrong answers, all different from each other and from `a` | yes |
| `e` | Short explanation shown after answering | yes |
| `s` | The exact handbook words that prove the answer (the 📖 line) | yes |
| `img` | A picture, relative to `img/`, e.g. `"signs/3-1-5.jpg"` | no |
| `o` | `true` for an official MTO sample question (shows ⭐) | no |

For **Pick the sign** questions (`"t": "pick"`), `a` and `w` are picture paths instead of text.

**Question types**

| Signs | Rules |
|---|---|
| `meaning` Sign meaning | `numbers` Exact numbers |
| `pick` Pick the sign | `row` Right-of-way |
| `lookalike` Look-alikes | `trap` Word traps |
| `shape` Shapes & colours | `best` Best action |
| `action` What do you do? | `law` Laws & consequences |

The answer order is shuffled automatically, so always put the right answer in `a`.

> **Heads-up:** each question's saved progress is linked to its question text, picture and right answer.
> Changing any of those makes it a "new" question for anyone who has already practised it.

## Sharing your changes

If you fixed a mistake or a rule changed, open an issue or a pull request on GitHub so everyone benefits.
Please include the handbook or ontario.ca link that backs it up.

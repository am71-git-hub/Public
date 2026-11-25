#!/usr/bin/env python3
"""Build printable HTML versions of the shortcut cheat sheets.

    python3 build.py            # build every sheet
    python3 build.py --no-fit   # skip auto-sizing (no Playwright needed)

Each ../windows/*.md and ../linux/*.md becomes <os>-<name>.html here, laid out
for US Letter landscape. With Playwright installed, each sheet's font size is
tuned to fit one page; if that would go below MIN_PT the sheet flows onto a
second page instead. Also writes help-desk-top-15.html (large print),
all.html (every sheet, one after another) and index.html.

Re-run after editing any .md file.
"""
import html
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SOURCES = [
    ("windows", "help-desk-data-entry"),
    ("windows", "text-selection-and-editing"),
    ("windows", "windows-desktop"),
    ("windows", "browser-chrome-edge"),
    ("windows", "teams"),
    ("windows", "office"),
    ("windows", "power-tools"),
    ("linux", "terminal-bash"),
    ("linux", "text-selection-and-clipboard"),
    ("linux", "gnome-desktop"),
]
MAX_PT, MIN_PT, STEP = 11.0, 7.0, 0.25
DEFAULT = {"fs": 8.0, "cols": 3}

KEY_WORDS = {
    "ctrl", "alt", "shift", "win", "super", "tab", "enter", "esc", "space", "home",
    "end", "insert", "delete", "backspace", "print", "prtscn", "pgup", "pgdn",
    "page up", "page down", "return", "menu", "←", "→", "↑", "↓",
}

# ── inline markdown ──────────────────────────────────────────────────────────

CODE_RE = re.compile(r"(?<!`)(`+)(?!`)(.+?)(?<!`)\1(?!`)")


def is_key(s):
    t = s.strip().lower()
    if " + " in s:
        return True
    if t in KEY_WORDS or re.fullmatch(r"f\d{1,2}", t):
        return True
    return len(t) == 1 or re.fullmatch(r"[a-z0-9]\s*/\s*[a-z0-9]", t) is not None


def render_code(s, in_key_cell):
    if s.startswith(" ") and s.endswith(" ") and s.strip():
        s = s[1:-1]
    if " + " in s or re.fullmatch(r"(Ctrl|Alt|Shift|Win|Super)(\+[^\s+]+)+", s):
        parts = s.split(" + ") if " + " in s else s.split("+")
        return '<span class="combo">' + '<i>+</i><wbr>'.join(
            f"<kbd>{html.escape(p)}</kbd>" for p in parts) + "</span>"
    if is_key(s) or (in_key_cell and len(s) <= 12 and " " not in s.strip()):
        return f"<kbd>{html.escape(s)}</kbd>"
    return f"<code>{html.escape(s)}</code>"


def render_text(s):
    s = html.escape(s, quote=False)
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)          # links -> text
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", s)
    return s


def inline(s, in_key_cell=False):
    # Swap code spans for placeholders so **bold** can wrap them, then restore.
    codes = []

    def stash(m):
        codes.append(render_code(m.group(2), in_key_cell))
        return f"\x00{len(codes) - 1}\x00"

    text = render_text(CODE_RE.sub(stash, s))
    return re.sub(r"\x00(\d+)\x00", lambda m: codes[int(m.group(1))], text)


# ── block markdown ───────────────────────────────────────────────────────────

def split_row(line):
    line = line.strip().strip("|")
    cells, cur, ticks = [], "", 0
    i = 0
    while i < len(line):
        c = line[i]
        if c == "\\" and i + 1 < len(line) and line[i + 1] == "|":
            cur += "|"
            i += 2
            continue
        if c == "|":
            cells.append(cur.strip())
            cur = ""
        else:
            cur += c
        i += 1
    cells.append(cur.strip())
    return cells


def parse(md):
    """Return (title, intro_html, list of section html strings)."""
    lines = md.splitlines()
    title, intro, sections = "", [], []
    cur = None  # list of html chunks for the current section
    i = 0

    def emit(chunk):
        (cur if cur is not None else intro).append(chunk)

    while i < len(lines):
        line = lines[i]
        s = line.strip()
        if s.startswith("# ") and not title:
            title = s[2:].strip()
        elif s.startswith("## "):
            if cur is not None:
                sections.append(cur)
            cur = [f"<h2>{inline(s[3:])}</h2>"]
        elif s.startswith("### "):
            emit(f"<h3>{inline(s[4:])}</h3>")
        elif s.startswith("```"):
            body = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                body.append(lines[i])
                i += 1
            emit(f"<pre>{html.escape(chr(10).join(body))}</pre>")
        elif s.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(split_row(lines[i]))
                i += 1
            i -= 1
            head, body = rows[0], [r for r in rows[2:]]
            t = ['<table>']
            if len(head) > 2:
                t.append("<thead><tr>" + "".join(f"<th>{inline(h)}</th>" for h in head) + "</tr></thead>")
            t.append("<tbody>")
            for r in body:
                t.append("<tr>" + "".join(
                    f"<td>{inline(c, in_key_cell=(j == 0))}</td>" for j, c in enumerate(r)) + "</tr>")
            t.append("</tbody></table>")
            emit("".join(t))
        elif re.match(r"^(\d+\.|-)\s", s):
            ordered = s[0].isdigit()
            start = int(s.split(".")[0]) if ordered else 1
            items = []
            while i < len(lines):
                ln = lines[i]
                if re.match(r"^\s*(\d+\.|-)\s", ln):
                    items.append(re.sub(r"^\s*(\d+\.|-)\s+", "", ln))
                elif ln.startswith(("  ", "\t")) and ln.strip() and items:
                    items[-1] += "<br>" + ln.strip()      # indented continuation line
                else:
                    break
                i += 1
            i -= 1
            tag = "ol" if ordered else "ul"
            attr = f' start="{start}"' if ordered and start != 1 else ""
            body = "".join("<li>" + "<br>".join(inline(p) for p in x.split("<br>")) + "</li>" for x in items)
            emit(f"<{tag}{attr}>{body}</{tag}>")
        elif s.startswith(">"):
            body = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                body.append(lines[i].strip().lstrip(">").strip())
                i += 1
            i -= 1
            emit(f'<p class="note">{inline(" ".join(body))}</p>')
        elif s == "---" or not s or s.startswith("Last updated"):
            pass
        else:
            body = [s]
            while (i + 1 < len(lines) and lines[i + 1].strip()
                   and not re.match(r"^(#|\||```|>|-\s|\d+\.\s|---)", lines[i + 1].strip())):
                i += 1
                body.append(lines[i].strip())
            emit(f"<p>{inline(' '.join(body))}</p>")
        i += 1
    if cur is not None:
        sections.append(cur)
    return title, "".join(intro), units(sections)


def units(sections):
    """Flatten sections into packable units: each heading sticks to the block after it."""
    out = []
    for chunks in sections:
        pending = ""
        for c in chunks:
            if c.startswith(("<h2>", "<h3>")):
                pending += c
            else:
                out.append(pending + c)
                pending = ""
        if pending:
            out.append(pending)
    return out


# ── page template ────────────────────────────────────────────────────────────

CSS = """
/* Monochrome by design: made for a black & white laser printer.
   No gradients, no colour, no grey fills (they print as dither dots).
   Hierarchy comes from weight, size, borders and italics only. */
:root {
  --paper: #FFFFFF; --ink: #000000; --rule: #000000; --desk: #E6E6E6; --toolbar: #333333;
  --mono: ui-monospace, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace;
  --sans: system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) { --desk: #161616; --toolbar: #BBBBBB; }
}
:root[data-theme="dark"] { --desk: #161616; --toolbar: #BBBBBB; }
@page { size: letter landscape; margin: 0.3in; }
* { box-sizing: border-box; }
html, body { margin: 0; background: var(--desk); color: var(--ink); font-family: var(--sans); }
body { padding: 16px; }
.toolbar { max-width: 10.4in; margin: 0 auto 12px; display: flex; gap: 12px; align-items: center;
  font-size: 14px; color: var(--toolbar); flex-wrap: wrap; }
.toolbar button { font: inherit; padding: 6px 14px; border: 1px solid #000; border-radius: 6px;
  background: #fff; color: #000; cursor: pointer; }
.toolbar a { color: inherit; }
.page { width: 10.4in; margin: 0 auto 24px; background: var(--paper); color: var(--ink); padding: 0;
  box-shadow: 0 1px 4px rgba(0,0,0,.25); font-size: var(--fs); line-height: 1.28;
  display: flex; flex-direction: column; }
.page.fit { height: 7.9in; overflow: hidden; }
.head { display: flex; align-items: baseline; justify-content: space-between; gap: 1em;
  border-bottom: 2.5pt solid var(--ink); padding: .1em .1em .25em; margin: 0 .6em; }
.head h1 { margin: 0; font-size: 1.6em; letter-spacing: -.01em; font-weight: 800; }
.head span { font-family: var(--mono); font-size: .85em; white-space: nowrap; }
.intro { padding: .35em .7em 0; font-style: italic; }
.intro p { margin: 0 0 .3em; }
section:first-child h2 { margin-top: .1em; }
.cols { column-count: var(--cols); column-gap: 1.3em; column-rule: .5pt solid var(--rule);
  padding: .45em .7em .5em; }
.page.fit .cols { flex: 1; min-height: 0; column-fill: auto; }
section { break-inside: auto; }
h2 { font-size: 1.12em; font-weight: 800; text-transform: uppercase; letter-spacing: .03em;
  margin: .7em 0 .25em; padding-bottom: .1em; border-bottom: 1.5pt solid var(--ink); break-after: avoid; break-inside: avoid; }
h3 { font-size: 1em; font-weight: 700; margin: .45em 0 .15em; text-decoration: underline;
  text-underline-offset: .15em; break-after: avoid; break-inside: avoid; }
p { margin: .2em 0 .35em; }
p.note { border-left: 2.5pt solid var(--ink); padding-left: .5em; font-style: italic; }
ul, ol { margin: .15em 0 .35em; padding-left: 1.3em; }
li { margin: .08em 0; }
table { width: 100%; table-layout: fixed; border-collapse: collapse; margin: .1em 0 .3em; }
tr { break-inside: avoid; }
td, th { overflow-wrap: break-word; vertical-align: top; padding: .16em .3em .16em 0; border-bottom: .75pt dotted var(--rule); text-align: left; }
th { font-size: .8em; text-transform: uppercase; letter-spacing: .04em; font-weight: 700;
  border-bottom: 1pt solid var(--rule); }
td:first-child { width: 42%; }
table.three td:first-child { width: 34%; }
td:nth-child(3) { font-style: italic; }
kbd, code { font-family: var(--mono); font-size: .9em; white-space: nowrap; color: var(--ink); }
kbd { display: inline-block; padding: 0 .3em; border: .75pt solid var(--ink); border-bottom-width: 1.75pt;
  border-radius: 3px; background: var(--paper); line-height: 1.25; font-weight: 600; }
code { padding: 0 .1em; white-space: normal; word-break: break-word; border-bottom: .75pt dashed var(--ink); }
.combo { white-space: normal; }
.combo i { font-style: normal; padding: 0 .12em; font-size: .85em; }
pre { font-family: var(--mono); font-size: .82em; border: .75pt solid var(--ink); padding: .4em .5em;
  margin: .2em 0 .4em; white-space: pre-wrap; break-inside: avoid; }
.big td { padding: .35em .5em .35em 0; }
@media print {
  html, body { background: #fff; padding: 0; }
  .toolbar { display: none; }
  .page { box-shadow: none; margin: 0; break-after: page; }
  .page:last-child { break-after: auto; }
}
@media screen and (max-width: 10.9in) {
  body { overflow-x: auto; }
}
"""


def page_html(title, intro, sections, os_name, fs, cols, fit=True, extra_class="", cont=False):
    secs = "".join(f"<section>{s}</section>" for s in sections)
    secs = secs.replace("<table><thead>", '<table class="three"><thead>')
    intro_html = f'<div class="intro">{intro}</div>' if intro and not cont else ""
    cls = "page fit" if fit else "page"
    label = f"{os_name} · shortcuts" + (" · continued" if cont else "")
    return (f'<div class="{cls} {extra_class}" style="--fs:{fs}pt;--cols:{cols}">'
            f'<div class="head"><h1>{html.escape(title)}</h1><span>{label}</span></div>'
            f'{intro_html}<div class="cols">{secs}</div></div>')


def document(doc_title, pages, back_link=True):
    tb = ('<div class="toolbar"><button onclick="window.print()">Print</button>'
          '<span>Letter, landscape · margins: Default · scale 100% · black &amp; white is fine</span>'
          + ('<a href="index.html">all sheets</a>' if back_link else "") + "</div>")
    return ("<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
            "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
            f"<title>{html.escape(doc_title)}</title>\n<style>{CSS}</style>\n</head>\n<body>\n"
            f"{tb}\n{''.join(pages)}\n</body>\n</html>\n")


def sheet_pages(job, st):
    """Render a sheet's pages from fitted settings: st = {fs, cols, groups, fit}."""
    return [page_html(job["title"], job["intro"], grp, job["os"], st["fs"], st["cols"], st["fit"],
                      job["cls"], cont=(n > 0))
            for n, grp in enumerate(st["groups"])]


# ── fitting ──────────────────────────────────────────────────────────────────

def fit_all(jobs):
    """Pick the largest font (and column count) that fits each sheet on as few
    pages as possible, splitting between sections when one page is not enough."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Playwright not installed: using default sizes (--no-fit behaviour)")
        return None
    out = {}
    with sync_playwright() as p:
        browser = p.chromium.launch()
        pg = browser.new_page(viewport={"width": 1100, "height": 900})
        pg.emulate_media(media="print")
        cache = {}

        def fits(job, secs, fs, cols, cont):
            k = (job["title"], tuple(secs), fs, cols, cont)
            if k not in cache:
                pg.set_content(document("", [page_html(job["title"], job["intro"], secs, job["os"],
                                                        fs, cols, True, job["cls"], cont)]))
                cache[k] = not pg.evaluate(
                    "() => { const c = document.querySelector('.cols');"
                    " if (c.scrollWidth > c.clientWidth + 1 || c.scrollHeight > c.clientHeight + 1) return true;"
                    " return [...c.querySelectorAll('td, th, pre')].some(e => e.scrollWidth > e.clientWidth + 1); }")
            return cache[k]

        def pack(job, fs, cols, max_pages):
            groups, cur = [], []
            for sec in job["sections"]:
                if fits(job, cur + [sec], fs, cols, bool(groups)):
                    cur.append(sec)
                elif cur and fits(job, [sec], fs, cols, True):
                    groups.append(cur)
                    cur = [sec]
                else:
                    return None
                if len(groups) >= max_pages:
                    return None
            return groups + [cur]

        for key, job in jobs.items():
            best = None
            for max_pages in (1, 2, 3):
                for cols in job["cols"]:
                    fs = job["max_pt"]
                    while fs >= MIN_PT:
                        groups = pack(job, fs, cols, max_pages)
                        if groups:
                            if best is None or fs > best["fs"]:
                                best = {"fs": fs, "cols": cols, "groups": groups, "fit": True}
                            break
                        fs -= STEP
                if best:
                    break
            if best is None:  # give up on fixed pages: one flowing page
                best = {"fs": 8.0, "cols": 3, "groups": [job["sections"]], "fit": False}
            pg.set_content(document("", sheet_pages(job, best)))
            pdf = pg.pdf(prefer_css_page_size=True, print_background=True)
            best["pages"] = len(re.findall(rb"/Type\s*/Page(?!s)", pdf))
            out[key] = best
            print(f"  {key:40s} {best['fs']:>5}pt  {best['cols']} cols  {best['pages']} page(s)")
        browser.close()
    return out


# ── main ─────────────────────────────────────────────────────────────────────

def main():
    do_fit = "--no-fit" not in sys.argv
    jobs = {}

    # Large-print "15 to learn first", pulled from the help desk sheet
    hd_md = (ROOT / "windows" / "help-desk-data-entry.md").read_text()
    m = re.search(r"## The 15 to learn first\n(.*?)\n---", hd_md, re.S)
    t, intro, _ = parse("# The 15 to learn first\n" + m.group(1).replace(
        "Learn these before anything else.", "Help desk · learn these before anything else."))
    lead, _, table = intro.partition("</p>")
    jobs["help-desk-top-15"] = dict(
        title=t, intro=lead + "</p>", os="Windows", cls="big", cols=(1,), max_pt=20.0,
        sections=[table.replace("<table>", '<table class="big three">')])

    for os_dir, name in SOURCES:
        t, intro, sections = parse((ROOT / os_dir / f"{name}.md").read_text())
        jobs[f"{os_dir}-{name}"] = dict(
            title=t, intro=intro, sections=sections, cls="", cols=(2, 3, 4), max_pt=MAX_PT,
            os="Windows" if os_dir == "windows" else "Linux")

    settings = fit_all(jobs) if do_fit else None
    if settings is None:
        settings = {k: {"fs": 14.0 if j["cls"] == "big" else DEFAULT["fs"],
                        "cols": 1 if j["cls"] == "big" else DEFAULT["cols"],
                        "groups": [j["sections"]], "fit": False} for k, j in jobs.items()}

    all_pages, index_rows = [], []
    for key, job in jobs.items():
        st = settings[key]
        pages = sheet_pages(job, st)
        (HERE / f"{key}.html").write_text(document(job["title"], pages))
        all_pages += pages
        n = st.get("pages", "?")
        index_rows.append(f'<tr><td><a href="{key}.html">{html.escape(job["title"])}</a></td>'
                          f'<td>{job["os"]}</td><td>{n}</td></tr>')

    (HERE / "all.html").write_text(document("All Shortcut Sheets", all_pages))
    index = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Printable Shortcut Sheets</title>
<style>{CSS}
.idx {{ max-width: 44rem; margin: 0 auto; background: var(--paper); padding: 1.5rem 1.75rem; font-size: 15px;
  box-shadow: 0 1px 4px rgba(0,0,0,.18); }}
.idx h1 {{ margin: 0 0 .25rem; font-size: 1.6rem; }} .idx a {{ color: var(--ink); }}
.idx td:first-child {{ width: auto; }} .idx td {{ padding: .45rem .5rem .45rem 0; }}
</style></head><body><div class="idx">
<h1>Printable shortcut sheets</h1>
<p>Open a sheet and press <kbd>Ctrl</kbd>+<kbd>P</kbd>. Settings: <b>Letter, Landscape</b>, margins <b>Default</b>,
scale <b>100%</b>. Made for black &amp; white: no colour or grey fills.
Or open <a href="all.html">all.html</a> to print every sheet in one go.</p>
<table><thead><tr><th>Sheet</th><th>OS</th><th>Pages</th></tr></thead><tbody>
{''.join(index_rows)}
</tbody></table>
<p class="note">Generated by <code>build.py</code> from the Markdown sheets. Edit the .md, then run
<code>python3 build.py</code>.</p>
</div></body></html>
"""
    (HERE / "index.html").write_text(index)
    print(f"wrote {len(jobs)} sheets + all.html + index.html to {HERE}")


if __name__ == "__main__":
    main()

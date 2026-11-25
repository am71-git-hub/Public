# cat — beginner tutorial

GNU coreutils 8.32 · works the same on basically every Linux/Unix box ever made.

Last updated: 2026-07-04

---

## What cat is for

`cat` is short for **concatenate**. It does one thing: read files (or stdin) and write their contents to stdout, in order. That one thing turns out to cover three everyday jobs:

1. **Look at a file** — `cat file.txt` dumps it to your terminal.
2. **Combine files** — `cat a.txt b.txt > both.txt` glues them together.
3. **Feed or capture a stream** — cat sits in pipelines, copies stdin to a file, or types a quick file for you without opening an editor.

It has no scrolling, no search, no editing. That's the point — it's a pipe fitting, not a viewer. For anything longer than a screen you'll usually want `less` instead.

---

## The 60-second tour

```bash
cat /etc/hostname            # print a file
cat file1.txt file2.txt      # print two files back to back
cat *.log                    # print every .log file in order
cat -n script.sh             # print with line numbers
```

That's 90% of real-world cat usage right there.

---

## Creating files with cat

No editor needed for a quick file:

```bash
cat > notes.txt              # type, then press Ctrl-D on a new line to finish
this is line one
this is line two
<Ctrl-D>
```

- `>` **overwrites** notes.txt
- `>>` **appends** instead:

```bash
cat >> notes.txt             # add more lines to the end
```

`Ctrl-D` at the start of a line means "end of input" — that's how you tell cat you're done typing.

### Heredocs — scripting a file's contents

In scripts (or when pasting a block into a terminal) use a heredoc so the content and the command travel together:

```bash
cat > ~/.config/thing/config.toml << 'EOF'
[settings]
color = "blue"
EOF
```

Quoting the `'EOF'` stops the shell from expanding `$variables` inside the block. Leave it unquoted (`<< EOF`) when you *want* expansion.

---

## Combining files (the actual "concatenate")

```bash
cat part1 part2 part3 > whole          # glue files together
cat header.csv data*.csv > merged.csv  # common CSV pattern
cat file.txt >> log.txt                # append one file onto another
```

Order matters — files are output in the order you list them. `cat *.csv` expands alphabetically.

---

## Useful flags

| Flag | What it does | When you'd use it |
|------|--------------|-------------------|
| `-n` | number every line | reading code, quoting a line to someone |
| `-b` | number only non-blank lines | same, but blanks don't count |
| `-s` | squeeze runs of blank lines into one | cleaning up spaced-out files |
| `-A` | show invisibles: tabs as `^I`, line ends as `$` | debugging whitespace bugs |
| `-E` | show `$` at end of each line | spotting trailing spaces |
| `-T` | show tabs as `^I` | tabs-vs-spaces confusion |

The whitespace ones earn their keep the first time a Makefile or YAML file fails "for no reason":

```bash
cat -A Makefile | head        # Makefile recipes NEED real tabs — now you can see them
cat -E config.yml             # trailing spaces show up before the $
```

---

## cat in pipelines

cat with no filename reads **stdin**, so it slots into pipes:

```bash
cat access.log | grep 404              # works, but see below
dmesg | cat -n                         # number any command's output
cat - file.txt                         # "-" means stdin: prepend typed/piped input to a file's output
```

### The "useless use of cat" thing

`cat file | grep foo` works but spawns an extra process for nothing — grep can open files itself:

```bash
grep foo file        # same result, one process
```

Nobody will arrest you for it, and starting a pipeline with `cat file |` is genuinely handy while you're building the pipeline up interactively. Just know `grep`, `sort`, `head`, `awk` etc. all take filenames directly.

---

## When NOT to use cat

| Instead of | Use | Because |
|-----------|-----|---------|
| `cat bigfile` | `less bigfile` | scroll, search with `/`, quit with `q` |
| `cat file \| head` | `head file` | head takes filenames |
| `cat binaryfile` | `xxd binaryfile \| less` | binary garbage can scramble your terminal¹ |
| `cat > file` for real editing | `nano` / `vim` | you can't fix a typo on a previous line |

¹ If your terminal ever gets scrambled by catting a binary, type `reset` and press Enter (even if you can't see what you're typing).

---

## The cat family

| Command | What it does |
|---------|--------------|
| `tac file` | cat backwards — last line first |
| `nl file` | number lines (more formatting options than `cat -n`) |
| `zcat file.gz` | cat a gzipped file without unzipping it |
| `head` / `tail` | just the first / last N lines |
| `tee` | like cat, but writes to a file *and* stdout at once |

```bash
zcat /var/log/syslog.2.gz | grep error    # read rotated logs in place
some-command | tee output.txt              # watch output AND save it
tac history.log | head -20                 # most recent 20 lines, newest first
```

---

## Practice exercises

```bash
cd /tmp
printf 'apple\nbanana\n' > a.txt
printf 'cherry\ndate\n' > b.txt

cat a.txt                    # 1. view one file
cat a.txt b.txt              # 2. view both, in order
cat a.txt b.txt > fruit.txt  # 3. merge them
cat -n fruit.txt             # 4. numbered
cat >> fruit.txt             # 5. type 'elderberry', Enter, Ctrl-D
cat -A fruit.txt             # 6. see the $ line endings
tac fruit.txt                # 7. reversed
```

---

## Further reading

- `man cat` — short, actually readable
- `cat --help` — one-screen flag summary
- `REFERENCE.md` in this folder — every flag, edge case, and family command
- `cat-cheatsheet.html` in this folder — printable one-pager

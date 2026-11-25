# cat In-Depth Reference

GNU coreutils 8.32 (Debian/Ubuntu) · POSIX-compatible everywhere

> Every flag, behavior, and edge case of `cat`, plus its close relatives. The beginner walkthrough lives in `README.md`; the printable one-pager is `cat-cheatsheet.html`.

---

## Table of Contents

1. [Synopsis & model](#1-synopsis--model)
2. [Complete flag reference](#2-complete-flag-reference)
3. [Reading: files, stdin, and `-`](#3-reading-files-stdin-and--)
4. [Writing: redirection patterns](#4-writing-redirection-patterns)
5. [Heredocs and herestrings](#5-heredocs-and-herestrings)
6. [Showing invisible characters](#6-showing-invisible-characters)
7. [cat in pipelines (and UUOC)](#7-cat-in-pipelines-and-uuoc)
8. [Binary files and terminal safety](#8-binary-files-and-terminal-safety)
9. [Exit status and errors](#9-exit-status-and-errors)
10. [The cat family](#10-the-cat-family)
11. [Recipes](#11-recipes)

---

## 1. Synopsis & model

```
cat [OPTION]... [FILE]...
```

cat opens each FILE in order and copies its bytes to stdout. That's the entire model:

```
FILE1 ──┐
FILE2 ──┼──►  stdout  (terminal, pipe, or redirected file)
stdin ──┘
```

- **No FILE, or FILE is `-`** → read stdin.
- Multiple files are output **in argument order** with nothing inserted between them (no separators, no filenames — compare `head`/`tail`, which print `==> name <==` headers for multiple files).
- cat never modifies its input files. All "writing" is done by the *shell's* redirection, not by cat itself.

---

## 2. Complete flag reference

| Flag | Long form | Effect |
|------|-----------|--------|
| `-n` | `--number` | Number all output lines, 1-indexed, right-aligned width 6, tab after |
| `-b` | `--number-nonblank` | Number only non-empty lines; **overrides `-n`** |
| `-s` | `--squeeze-blank` | Collapse runs of 2+ blank lines into a single blank line |
| `-E` | `--show-ends` | Print `$` at the end of every line (before the newline) |
| `-T` | `--show-tabs` | Print TAB characters as `^I` |
| `-v` | `--show-nonprinting` | Show control chars as `^X`, high-bit chars as `M-x` (except LF and TAB) |
| `-e` | — | Equivalent to `-vE` |
| `-t` | — | Equivalent to `-vT` |
| `-A` | `--show-all` | Equivalent to `-vET` — the "show me everything" flag |
| `-u` | — | Ignored (POSIX relic; output is already unbuffered as needed) |
| | `--help` | Usage summary |
| | `--version` | Version info |

Notes:

- `-b` + `-n` together: `-b` wins. Blank lines get no number and don't advance the counter.
- Line numbers reset per *invocation*, not per file — `cat -n a b` numbers continuously across both files.
- `-s` considers a line blank only if it is *completely* empty. A line containing one space is not blank (use `cat -A` to spot those).
- None of the "show" flags escape the newline itself — every line still ends with a real LF.

---

## 3. Reading: files, stdin, and `-`

```bash
cat file                 # one file
cat file1 file2          # in order
cat                      # stdin until Ctrl-D (interactive) or EOF (pipe)
cat -                    # same: '-' is an explicit alias for stdin
cat header - footer      # stdin sandwiched between two files
cat -- -weirdname        # a real file literally named "-weirdname"
```

- `-` may appear **multiple times**, but stdin is consumed the first time — later `-` args read nothing more from a pipe.
- `--` ends option parsing; needed for filenames starting with `-`.
- Reading a directory is an error: `cat: dir: Is a directory` (exit 1, other files still print).
- cat follows symlinks and happily reads device/special files: `cat /dev/urandom` (don't, see §8), `cat /proc/cpuinfo` (very useful).

### /proc and /sys — cat as a system inspector

Many "files" on Linux are kernel state; cat is the canonical way to read them:

```bash
cat /proc/cpuinfo
cat /proc/meminfo
cat /sys/class/power_supply/BAT0/capacity     # battery % (laptops)
cat /sys/class/backlight/*/brightness
cat /etc/os-release
```

---

## 4. Writing: redirection patterns

The shell does the writing; cat just supplies the stream.

| Pattern | Effect |
|---------|--------|
| `cat a b > out` | concatenate into `out` (truncates first) |
| `cat a >> out` | append `a` onto `out` |
| `cat > out` | create/overwrite `out` from typed stdin (end with Ctrl-D) |
| `cat >> out` | append typed stdin |
| `cat a \| cmd` | feed a file to a command (see UUOC, §7) |

**Trap — self-reference:** `cat a b > a` truncates `a` *before* cat reads it. You lose `a`'s contents. Use a temp file, or `sponge` from moreutils:

```bash
cat a b | sponge a       # sponge soaks up all input before writing
```

**Trap — sudo:** redirection happens in *your* shell, not under sudo. `sudo cat file > /root/out` fails. Use tee:

```bash
cat file | sudo tee /root/out > /dev/null
```

---

## 5. Heredocs and herestrings

Heredocs are shell syntax, but `cat` is their most common partner.

```bash
cat << EOF               # expanded: $HOME, $(date), backslashes are processed
Current home: $HOME
EOF

cat << 'EOF'             # quoted delimiter = literal, nothing expanded
This $HOME stays as-is.
EOF

cat <<- EOF              # <<- strips leading TABs (not spaces) — indented scripts
	indented in source,
	flush in output
EOF

cat <<< "one-liner"      # herestring: a single string as stdin
```

Combined with redirection — the standard "write a config from a script" idiom:

```bash
cat > /etc/systemd/system/thing.service << 'EOF'
[Unit]
Description=thing
EOF
```

The delimiter (`EOF` here, any word works) must be alone on its own line, no trailing spaces.

---

## 6. Showing invisible characters

The `-A` family answers "why does this file misbehave?"

```bash
cat -A file
```

| You see | It means |
|---------|----------|
| `^I` | a TAB character |
| `$` at line end | end of line (LF); text before it = trailing whitespace |
| `^M$` at line end | CRLF — a Windows/DOS line ending |
| `M-`something | byte with the high bit set (often UTF-8 seen byte-by-byte) |
| `^[` | ESC — start of an ANSI color code |

Classic diagnoses:

```bash
cat -A Makefile           # recipe lines MUST start with ^I (tab), not spaces
cat -A script.sh | head   # ^M$ everywhere → CRLF; fix: dos2unix script.sh
cat -E data.csv           # "identical" strings differ? trailing space before $
```

Note `-v` renders UTF-8 multibyte chars as `M-` gibberish — it shows *bytes*, not characters. For proper byte inspection use `xxd` or `od -c`.

---

## 7. cat in pipelines (and UUOC)

cat is a legitimate pipeline citizen when it's actually concatenating or adapting:

```bash
cat *.log | sort | uniq -c            # genuinely merging many files
dmesg | cat -n                        # borrowing -n for another command's output
cat - footer.txt                      # stdin + file combined
```

**UUOC** ("useless use of cat") is `cat file | cmd` where `cmd` accepts a filename or redirection:

```bash
cat file | grep pat      # → grep pat file
cat file | wc -l         # → wc -l < file
cat file | head -5       # → head -5 file
```

Cost: one extra process and pipe copy. Verdict: irrelevant interactively, worth fixing in scripts and hot loops. One honest defense: `cat file |` at the head of a pipeline makes it easy to iterate on the rest, and reads left-to-right.

---

## 8. Binary files and terminal safety

Catting a binary sends raw control bytes to your terminal. Some (like ESC sequences) can switch character sets and leave the display scrambled after cat exits.

- **Fix a scrambled terminal:** type `reset` and Enter (blind typing is fine), or `stty sane`, or `printf '\033c'`.
- **Inspect binaries properly:**

```bash
xxd file | less          # hex + ASCII columns
od -c file | less        # octal/char dump
strings file | less      # printable runs only
file whatever            # what IS this, before catting it
```

- `cat -v binary` is *safer* (control chars become visible `^X` notation) but still not a real hex view.

---

## 9. Exit status and errors

| Exit | Meaning |
|------|---------|
| `0` | all inputs read and written successfully |
| `1` | any error: missing file, permission denied, is-a-directory, write error |

- On a per-file error, cat prints a message to stderr and **continues with the remaining files** — exit is still 1 at the end.
- `cat: write error: Broken pipe` / silent death happens when the reader quits early (`cat huge | head`). Harmless and normal — head got what it needed.
- Errors go to stderr, so `cat a missing b > out 2> errs` captures content and complaints separately.

---

## 10. The cat family

| Command | Package | Purpose |
|---------|---------|---------|
| `tac` | coreutils | Lines in reverse order (last line first) |
| `nl` | coreutils | Line numbering with real control (styles, formats, sections) |
| `head` / `tail` | coreutils | First / last N lines; `tail -f` follows growth |
| `tee` | coreutils | Split a stream: write to file(s) *and* pass through stdout |
| `zcat` `bzcat` `xzcat` `zstdcat` | compression pkgs | cat through a decompressor — read `.gz`/`.bz2`/`.xz`/`.zst` in place |
| `less` | less | The pager — what you actually want for *reading* |
| `paste` | coreutils | Side-by-side (column-wise) merge — cat is end-to-end, paste is left-to-right |
| `split` | coreutils | The inverse: cut one file into pieces (`cat` the pieces to rebuild) |
| `sponge` | moreutils | Buffer whole input before writing — enables `... | sponge samefile` |
| `bat` | bat (extra install) | "cat with wings": syntax highlighting, git margins, auto-paging |

`nl` vs `cat -n` in one line: `nl` skips blank lines by default (like `cat -b`) and has `-w` width, `-s` separator, `-ba` to number all.

```bash
zcat /var/log/syslog.*.gz | grep -i error     # search rotated logs without extracting
make 2>&1 | tee build.log                     # watch AND record a build
split -b 100M big.iso part_ && cat part_* > big.iso   # split / rebuild round-trip
```

---

## 11. Recipes

```bash
# merge CSVs, keeping only the first header
head -1 first.csv > merged.csv && tail -n +2 -q *.csv >> merged.csv

# quick multi-line file without an editor
cat > /tmp/hosts.txt << 'EOF'
192.168.1.10  desktop
192.168.1.20  server
EOF

# number a file permanently
cat -n draft.txt > numbered.txt

# strip the CRLF a Windows editor left behind (view first, then fix)
cat -A file.txt | head
sed -i 's/\r$//' file.txt

# empty a file you don't own the writing habit for (keeps inode/permissions)
: > /var/log/app.log          # note: pure shell, no cat needed
cat /dev/null > file          # same effect, classic spelling

# concatenate with filename headers (cat itself can't; use tail or head)
tail -n +1 file1 file2       # prints ==> file1 <== style headers

# read a file into a shell variable
data=$(cat file)              # classic
data=$(< file)                # bash builtin, no process — faster
```

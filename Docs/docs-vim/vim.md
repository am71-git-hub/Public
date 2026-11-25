# Vim

Vim is a modal text editor: the keyboard does different things depending on which *mode* you're in. That one idea explains almost everything. Once it clicks, Vim becomes faster than any editor you've used before because your hands never leave the home row.

---

## The Mental Model

Vim editing is a **language**. It has:

- **Verbs** — what to do (`d` delete, `c` change, `y` yank, `>` indent)
- **Modifiers** — how far (`i` inside, `a` around)
- **Nouns** — what to act on (`w` word, `s` sentence, `p` paragraph, `"` quotes, `{` braces)

Combine them: `diw` = delete inside word. `ca"` = change around quotes. `>ap` = indent around paragraph. You're not memorizing commands — you're learning grammar.

---

## Modes

| Mode | How to Enter | What It Does |
|------|-------------|--------------|
| **Normal** | `Esc` or `Ctrl-[` | Navigate and issue commands — your home base |
| **Insert** | `i`, `a`, `o`, `I`, `A`, `O` | Type text |
| **Visual** | `v`, `V`, `Ctrl-v` | Select text for an operation |
| **Command** | `:` | Run ex commands (save, quit, search/replace) |
| **Replace** | `R` | Overtype text |
| **Operator-pending** | (after a verb) | Waiting for a motion/noun |

**Rule:** Press `Esc` when in doubt. You can never break anything from Normal mode.

---

## Getting Started in 10 Minutes

### 1. Open a file
```
vim filename.txt
```

### 2. You start in Normal mode. Move around:
```
h j k l    ←  ↓  ↑  →
w          jump forward one word
b          jump back one word
0          start of line
$          end of line
gg         top of file
G          bottom of file
```

### 3. Enter Insert mode and type:
```
i    insert before cursor
a    insert after cursor
o    open new line below and insert
```

### 4. Back to Normal, make changes:
```
x      delete character under cursor
dd     delete entire line
u      undo
Ctrl-r redo
```

### 5. Save and quit:
```
:w     save
:q     quit
:wq    save and quit
:q!    quit without saving
```

That's it. You can now survive in Vim.

---

## What You Can Do — Full Picture

### Text Objects (the nouns)
```
iw / aw    inside/around word
is / as    inside/around sentence
ip / ap    inside/around paragraph
i" / a"    inside/around double quotes
i' / a'    inside/around single quotes
i( / a(    inside/around parentheses  (also ib)
i{ / a{    inside/around braces       (also iB)
i[ / a[    inside/around brackets
it / at    inside/around HTML tag
```

### Motions (how far to move)
```
w / W      next word (W ignores punctuation)
b / B      previous word
e / E      end of word
f{char}    jump to next char on line
t{char}    jump to just before next char
; / ,      repeat / reverse last f/t
%          jump to matching bracket/paren/brace
{ / }      previous/next blank line (paragraph)
( / )      previous/next sentence
[[ / ]]    previous/next function/section
```

### Operators (the verbs)
```
d    delete (also cuts to register)
c    change (delete + enter insert mode)
y    yank (copy)
>    indent right
<    indent left
=    auto-indent
gu   lowercase
gU   uppercase
g~   toggle case
```

Operators + motions = power:
```
dw      delete to next word
d$      delete to end of line  (same as D)
ci"     change text inside quotes
yip     yank paragraph
=G      auto-indent from cursor to end of file
```

### Search
```
/pattern     search forward
?pattern     search backward
n            next match
N            previous match
*            search for word under cursor (forward)
#            search for word under cursor (backward)
```

### Search & Replace
```
:s/old/new/        replace first on current line
:s/old/new/g       replace all on current line
:%s/old/new/g      replace all in file
:%s/old/new/gc     replace all, confirm each
:%s/\bword\b/new/g replace whole words only
```

### Registers (clipboard)
```
yy          yank line into default register
"ayy        yank line into register a
"ap         paste from register a
"+y         yank to system clipboard
"+p         paste from system clipboard
:reg        show all registers
```

### Macros
```
qa          start recording macro into register a
q           stop recording
@a          replay macro a
@@          replay last macro
5@a         replay macro a 5 times
```

### Marks
```
ma          set mark a at current position
`a          jump to mark a (exact position)
'a          jump to line of mark a
``          jump back to position before last jump
'.          jump to last edit position
:marks      list all marks
```

### Windows / Splits
```
:sp filename    horizontal split
:vsp filename   vertical split
Ctrl-w h/j/k/l  navigate between splits
Ctrl-w =        equalize split sizes
Ctrl-w _        maximize height of current split
Ctrl-w |        maximize width of current split
:only           close all splits except current
```

### Tabs
```
:tabnew filename    open in new tab
gt                  next tab
gT                  previous tab
:tabc               close tab
```

### Buffers
```
:e filename     open file (new buffer)
:ls             list open buffers
:b2             switch to buffer 2
:bn / :bp       next / previous buffer
:bd             delete (close) buffer
```

### Folding
```
zf{motion}    create fold
zo / zc       open / close fold
za            toggle fold
zR / zM       open all / close all folds
```

---

## Structure of Vim Configuration

```
~/.vimrc               main config file (or ~/.vim/vimrc)
~/.vim/
  plugin/              manually dropped .vim plugin files
  autoload/            lazy-loaded scripts
  colors/              color schemes
  after/               overrides loaded after everything else
  ftplugin/            filetype-specific settings (e.g. python.vim)
  syntax/              custom syntax files
  pack/                native package manager (Vim 8+)
    vendor/
      start/           plugins loaded automatically
      opt/             plugins loaded on demand with :packadd
```

**Neovim** uses `~/.config/nvim/init.vim` (or `init.lua`) and `~/.config/nvim/` in place of `~/.vim/`.

---

## Categorized Cheat Sheet

### Navigation

| Key | Action |
|-----|--------|
| `h j k l` | left / down / up / right |
| `w W b B e E` | word forward/back/end |
| `0 ^ $` | line start (col 0) / first non-blank / end |
| `gg G` | file top / bottom |
| `{N}G` | go to line N |
| `Ctrl-d Ctrl-u` | half-page down / up |
| `Ctrl-f Ctrl-b` | full page down / up |
| `zz zt zb` | center / top / bottom current line in view |
| `H M L` | cursor to screen top / middle / bottom |
| `%` | jump to matching bracket |

### Inserting Text

| Key | Action |
|-----|--------|
| `i / I` | insert before cursor / before line |
| `a / A` | insert after cursor / end of line |
| `o / O` | new line below / above |
| `s / S` | substitute char / line (delete + insert) |
| `r{char}` | replace single character |
| `R` | enter replace (overtype) mode |

### Editing

| Key | Action |
|-----|--------|
| `x X` | delete char under / before cursor |
| `dd D` | delete line / to end of line |
| `cc C` | change line / to end of line |
| `yy Y` | yank line |
| `p P` | paste after / before cursor |
| `u Ctrl-r` | undo / redo |
| `.` | repeat last change |
| `J` | join line below to current |
| `>>  <<` | indent / dedent line |
| `~` | toggle case of character |

### Visual Mode

| Key | Action |
|-----|--------|
| `v` | character-wise visual |
| `V` | line-wise visual |
| `Ctrl-v` | block visual |
| `o` | move to other end of selection |
| `gv` | reselect last visual selection |
| After selecting: `d y c > < =` | delete/yank/change/indent/etc. |

### Search & Navigation

| Key | Action |
|-----|--------|
| `/pat ?pat` | search forward / backward |
| `n N` | next / previous match |
| `* #` | search word under cursor fwd / bwd |
| `f{c} F{c}` | find char on line forward / backward |
| `t{c} T{c}` | to (before) char forward / backward |
| `; ,` | repeat / reverse last f/t |

### Files & Buffers

| Command | Action |
|---------|--------|
| `:e {file}` | edit file |
| `:w` | write (save) |
| `:wa` | write all buffers |
| `:q :wq :q!` | quit / save+quit / force quit |
| `:ls` | list buffers |
| `:b{N}` | switch to buffer N |
| `:bd` | delete buffer |
| `Ctrl-^` | toggle last two buffers |

### Windows

| Key / Command | Action |
|--------------|--------|
| `:sp :vsp` | horizontal / vertical split |
| `Ctrl-w s/v` | split shortcut |
| `Ctrl-w hjkl` | navigate splits |
| `Ctrl-w + - < >` | resize splits |
| `Ctrl-w =` | equalize sizes |
| `:only` | close other splits |

### Useful Ex Commands

| Command | Action |
|---------|--------|
| `:!{cmd}` | run shell command |
| `:r {file}` | read file into buffer |
| `:r !{cmd}` | read command output into buffer |
| `:%y+` | yank whole file to clipboard |
| `:set {option}` | set an option |
| `:set no{option}` | unset an option |
| `:set {option}?` | check option value |
| `:noh` | clear search highlight |
| `:retab` | convert tabs/spaces per current settings |

### Useful Options (put in .vimrc)

```vim
set number          " line numbers
set relativenumber  " relative line numbers (great with j/k counts)
set hlsearch        " highlight search matches
set incsearch       " incremental search
set ignorecase      " case-insensitive search...
set smartcase       " ...unless pattern has uppercase
set expandtab       " spaces instead of tabs
set tabstop=4       " tab = 4 spaces
set shiftwidth=4    " indent = 4 spaces
set autoindent
set wrap            " wrap long lines
set scrolloff=8     " keep 8 lines above/below cursor
set wildmenu        " command completion menu
set clipboard=unnamedplus  " use system clipboard
set undofile        " persistent undo across sessions
```

---

## Learning Path — What to Do Next

```
Phase 1 — Survival (you are here)
├── Navigate with h/j/k/l and w/b
├── Enter and exit insert mode
├── Save and quit :wq :q!
└── Undo with u

Phase 2 — Fluency
├── Use . (dot) to repeat changes
├── Learn text objects: diw, ci", ya(
├── Learn f/t navigation on a line
├── Use * to search word under cursor
└── Learn :s for substitution

Phase 3 — Power User
├── Record and replay macros (qa ... q then @a)
├── Use visual block mode Ctrl-v for column edits
├── Use marks (ma, `a) for jumping
├── Learn window splits (:sp :vsp)
├── Use numbered registers and "+ clipboard
└── Write a .vimrc with your settings

Phase 4 — Customization
├── Write your own .vimrc keymaps (nnoremap etc.)
├── Install a plugin manager (vim-plug, lazy.nvim)
├── Add plugins: fuzzy finder, file tree, git integration
├── Add a colorscheme
├── Configure filetype-specific settings in ftplugin/
└── Try Neovim + Lua config for modern tooling

Phase 5 — Mastery
├── Understand the expression register (Ctrl-r =)
├── Write Vimscript or Lua functions
├── Use :autocmd for event-driven behavior
├── Learn :g and :v (global commands) for bulk edits
│     :g/pattern/d    — delete all matching lines
│     :v/pattern/d    — delete all non-matching lines
├── Use :norm to apply normal-mode commands to ranges
│     :%norm A;       — append ; to every line
└── Build custom text objects and operators with plugins
```

---

## Survival Cheatsheet (print this)

```
MOVE        h←  j↓  k↑  l→   gg top   G bot   {N}G line N
WORD        w next   b back   e end
LINE        0 start  ^ nonblank  $ end
PAGE        Ctrl-d half-dn   Ctrl-u half-up

INSERT      i before  a after  o newline below  O newline above
CHANGE      r{c} replace char   s subst char   cc change line   C change→end
DELETE      x del char   dd del line   D del→end
YANK/PASTE  yy yank line   p paste after   P paste before
UNDO        u undo   Ctrl-r redo   . repeat

SEARCH      /pat  n next  N prev  * word-under-cursor
REPLACE     :%s/old/new/gc

SAVE/QUIT   :w  :q  :wq  :q!
```

---

## Related

- `/tmux` — run Vim inside tmux panes/windows for multi-file workflows
- `vimtutor` — built-in interactive tutorial, run it in your terminal

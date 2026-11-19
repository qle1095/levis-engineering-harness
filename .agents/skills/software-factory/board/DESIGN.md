# Board design

How the board looks and why. Read this before changing `board.html`.

The board is a developer tool. It should feel like a CI console or an issue tracker a developer keeps open all day: quiet, dense, exact. Think of the run list in a CI system and the issue list in a modern tracker. It should not look like a generated dashboard.

## The one idea

A ticket is a row, and its stage is a pipeline drawn in that row. The board is a list of rows, most urgent first. There are no columns of cards.

A list is denser than cards, it sorts by urgency, and a pipeline in each row shows where the ticket is and how far it has to go. Tickets that need Levi are at the top, because that is the first thing he looks for.

## Rules

1. **Neutral first.** The interface is greyscale. Colour means state and nothing else. There is one accent colour, used only for focus and selection.
2. **Hierarchy from weight and grey level.** Not from size, capitals, or boxes. Three text levels: primary, secondary, tertiary.
3. **Hairlines, not boxes.** Rows are separated by 1px lines. No cards, no shadows, no tinted fills. Corner radius is at most 6px.
4. **Mono for data, sans for words.** Ids, numbers, paths, verdicts, and model names are monospace. Everything a person reads as a sentence is sans.
5. **State is a glyph and a word.** A small shape in the state colour, then plain text. Never a pill, never a tinted badge.
6. **Every number has a column header.** Nothing on the board needs a legend to read.
7. **Keyboard first.** Every action has a key, and the keys are shown.
8. **Still unless something is running.** The only motion is the spinner on a working ticket. Transitions are 120ms. Honour reduced motion.

## Never

- Gradients, glows, drop shadows, or decorative stripes.
- Pills, tinted badges, or coloured left borders.
- Letter-spaced capitals.
- A different colour for each stage.
- Emoji.
- Cards inside cards, or a border inside a border.
- A legend bar.
- Centred hero text. An empty board says one line and shows the command.
- More than one accent colour.

## Tokens

Both themes follow the system setting. Define these as CSS variables and use nothing else.

| Token | Dark | Light | Use |
| --- | --- | --- | --- |
| `--bg` | `#0b0b0c` | `#ffffff` | Page |
| `--surface` | `#121214` | `#fafafa` | Hovered row, pane header |
| `--raised` | `#18181b` | `#f4f4f5` | Selected row, code blocks |
| `--border` | `#232326` | `#e8e8ea` | Hairlines |
| `--border-strong` | `#34343a` | `#d4d4d8` | Inputs, pipeline nodes not yet reached |
| `--text` | `#ededef` | `#111113` | Primary text |
| `--text-2` | `#a1a1aa` | `#5f5f68` | Secondary text, data |
| `--text-3` | `#6c6c76` | `#9a9aa3` | Tertiary text, headers, placeholders |
| `--accent` | `#7c8cff` | `#4353e0` | Focus ring, selected row marker, links |
| `--working` | `#4c9aff` | `#1f6fe5` | A sub-agent is on it |
| `--waiting` | `#e5a50a` | `#b07800` | Waiting on Levi |
| `--stopped` | `#f85149` | `#d1242f` | The line cannot continue |
| `--done` | `#3fb950` | `#1a7f37` | Accepted, passed |
| `--quiet` | `#6c6c76` | `#9a9aa3` | No update for twenty minutes |

Verdicts reuse the state colours: READY, PASS, ACCEPT, DONE are `--done`. FAIL, REJECT, BLOCKED are `--stopped`. NEEDS-LEVI is `--waiting`.

**Type.** Sans: `Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif`. Mono: `"JetBrains Mono", "SF Mono", ui-monospace, Menlo, Consolas, monospace`. Load no web font; the board makes no request outside localhost. Base size 13px, line height 1.5. Sizes in use: 11, 12, 13, 15. Numbers are tabular.

**Space.** A 4px grid. Row padding 8px by 16px. The page has no outer margin; the list runs edge to edge.

## Layout

```
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│ factory   ~/.software-factory        2 need you · 3 running · 5 done today · $4.31   ● live  ? │
├──────────────────────────────────────────────────────────────────────────────────────────┤
│ / Filter tickets                                    All  Needs you  Running  Done        │
├───────────────────────────────────────────────────────────────┬──────────────────────────┤
│ Ticket                     Pipeline      Round  Cost  Tokens  │  detail pane             │
│ Needs you  2                                                  │  (only when a ticket     │
│ ◉ Cache supplier price…    ●─●─○─○─○─○  research  …          │   is selected)           │
│ Running  3                                                    │                          │
│ ◌ Fix 500 on empty cart…   ●─·─●─●─◉─○  review    2/4 …      │                          │
│ Done  5                                                       │                          │
├───────────────────────────────────────────────────────────────┴──────────────────────────┤
│ j k move · enter open · esc close · / filter · ? help                                    │
└──────────────────────────────────────────────────────────────────────────────────────────┘
```

### Top bar

One line, 44px. Left: the word `factory` in mono, then the factory home path in tertiary text, with the home folder shortened to `~`. Right: counts as plain text separated by middle dots, then the live indicator, then a `?` button.

- Counts: need you (waiting plus stopped), running, done today, API cost of today's tickets. A count of zero is tertiary text. "need you" is in `--waiting` when it is not zero.
- Live indicator: a 6px dot and the word `live` in `--done`. When the board cannot reach the server, the dot and the words `offline` are `--stopped`.

### Filter row

One line, 40px. Left: a borderless text input with the placeholder `Filter tickets`, focused by `/`. It matches the title, id, repo, kind, and stage. Right: a segmented control, `All`, `Needs you`, `Running`, `Done`, each with its count in tertiary text. The chosen segment has primary text and a 1px underline in `--text`. No filled buttons.

### The list

Sticky column header, then groups. Group order: **Needs you**, **Running**, **Done**. A group with no tickets is not drawn. Group headers are sticky under the column header: the name in secondary text, 12px, weight 500, then the count in tertiary text, on `--bg`, with a hairline under them.

- **Needs you**: waiting and stopped tickets. Stopped first, then waiting, newest update first.
- **Running**: working and quiet tickets, newest update first.
- **Done**: newest first. Show ten, then a `Show all n` text button.

Columns, left to right:

| Column | Width | Content |
| --- | --- | --- |
| Ticket | flexible, at least 320px | Two lines. Line 1: the state glyph, then the title in primary text, weight 500. Line 2 in tertiary text, 12px, one line, cut with an ellipsis: kind, repo, then the latest update. When the ticket is waiting, stopped, or quiet, line 2 starts with the state in words, in the state colour: `Waiting on you`, `Stopped`, `Quiet 34m`. A working or done ticket has no state word: the glyph and the group already say it. |
| Pipeline | 208px | The pipeline, then the stage name in mono 12px secondary text. Wide enough for `verification`. |
| Round | 56px | `2/4` in mono. A dash before the first round. |
| Cost | 64px | `$1.12` |
| Tokens | 64px | `1.2M` |
| Time | 56px | Time on the line: `3m`, `1h 12m` |
| Model | 96px | `opus-5-5` |
| Updated | 64px | `now`, `2m`, `1h`, `3d`. No "ago". |

Data columns are mono, 12px, secondary text, right-aligned, except Model, which is left-aligned. A value that does not exist yet is a dash in tertiary text. Column headers are 11px tertiary text, sentence case, aligned like their column.

Rows are 52px. Hover: `--surface`. Selected: `--raised`, with a 2px `--accent` line inset on the left edge, drawn as a pseudo-element and not as a border. A row never shows a focus outline; selection is its focus. The whole row is one button.

When the list is narrower than the columns need, drop columns in this order: Model, Tokens, Time, Cost. Below 720px drop Round and Updated too, and put the pipeline under the title. Measure the list, not the window: the list narrows when the detail pane opens.

### State glyph

12px, drawn in SVG with `currentColor`, in the state colour.

| State | Glyph |
| --- | --- |
| Working | A ring with a quarter arc that spins, 1s linear |
| Waiting on you | A filled circle with a ring around it |
| Stopped | A filled square with 2px corners |
| Quiet | A hollow circle, 1.5px stroke |
| Done | A check mark, 1.75px stroke, round caps |

### Pipeline

Six nodes on a line, one per stage: intake, research, verification, build, review, done. Nodes are 8px circles, 20px apart, joined by a 1px line.

| Node | Drawn as |
| --- | --- |
| A stage already passed | Filled `--text-2`. The line to the next node is `--text-2` |
| The current stage | Filled with the ticket's state colour, with a 3px ring of the same colour at 25% opacity. On a working ticket the ring pulses |
| A stage not yet reached | Hollow, 1px `--border-strong`. The line to it is `--border` |
| Research on a standard ticket | A 4px dot in `--border-strong`. The ticket skips it |
| Every node on a done ticket | Filled `--done`. Research on a standard ticket stays the small dot: the ticket never went there |

Each node has a title attribute with its stage name. The pipeline is not a rainbow: a stage has no colour of its own.

### Detail pane

Opens on the right when a ticket is selected. Width 46% of the window, at least 520px, at most 760px, with a hairline on its left. The list stays usable beside it. Below 1100px it covers the list.

From the top:

1. **Header.** The title, 15px, weight 600. A ghost close button at the right, `esc` in tertiary text beside it. Under the title: the id in mono tertiary text. Clicking the id copies it and shows `copied` for a second.
2. **Facts.** One definition grid, four columns, labels in tertiary 11px, values in mono 12px: State, Stage, Kind, Round, Cost, Tokens, Time, Model, Repo, Opened, Updated. The state value has its glyph and colour. Repo shows the folder name, with the full path in the title attribute.
3. **Pipeline.** The same pipeline, larger: 10px nodes, spread across the pane, with each stage name under its node in 11px. The current stage name is primary text; the rest are tertiary.
4. **Tabs.** `Activity`, `Files n`, `Agents n`. Same look as the segmented control. Keys `1`, `2`, `3` switch them.

**Activity tab.** If the ticket has rounds, a small table first: Round, Build, Gate, Review. Each cell is the verdict word in mono, in its verdict colour, or a dash. Then the updates, newest first, as rows: time in mono tertiary (`22:41`), stage in mono secondary, then the note in primary text. A hairline between rows. No dots, no vertical rail.

**Files tab.** Two parts side by side. Left, 240px: the file list in mono 12px, one per row, with the verdict word right-aligned in its colour. A file name is not cut unless it is unusually long. Round folders are grouped under a `round 1` label in tertiary text. The open file's row is `--raised`. Right: the file. `request.md` is open first.

- Markdown files are rendered: headings as 13px weight 600, paragraphs, lists, tables with hairlines, fenced code in `--raised`. Render `**bold**` as bold and `` `code` `` as mono on `--raised`. Nothing else inline.
- A file's verdict line is shown above the document as plain mono text in its verdict colour, not as a badge.
- `.sh`, `.log`, and code files are shown in a mono block with line numbers in tertiary text.

**Agents tab.** A table: Sub-agent, Model, In, Out, Cost, Time. Numbers right-aligned in mono. A total row. Under it, one line of tertiary text: the cost is the API list price of the sub-agents, the orchestrator chat is not counted, and on a subscription it is relative spend, not a bill. If a model has no price, name it there.

5. **Footer.** The ticket folder path in mono tertiary text. Clicking copies it.

### Key bar

One line at the bottom, 28px, tertiary 11px text: `j` `k` move, `enter` open, `esc` close, `/` filter, `1` `2` `3` tabs, `?` help. Each key is in a small box: 1px `--border-strong`, 3px radius, mono.

### Help

`?` opens a small panel over the page, 420px wide, with a hairline border on `--surface`. It lists the five states with their glyphs and one line each, what a round is, how to read the pipeline, and the keys. `esc` or `?` closes it.

### Empty and broken states

- No tickets: one line of secondary text, left-aligned under the header, `No tickets yet.` Under it, in mono tertiary text, how to open one: invoke `software-factory` with a task.
- No tickets match the filter: `No tickets match "<text>".`
- A ticket file the board cannot read: one line above the list in `--stopped` naming the ticket.
- Server unreachable: the live indicator changes. The list keeps what it last showed.

## Behaviour to keep

- The page asks `/api/tickets` every two seconds and redraws only when something changed.
- A working ticket with no update for twenty minutes is shown as quiet.
- The tab title starts with the number of tickets that need Levi.
- Every string from a ticket is put on the page as text, never as HTML.
- The selected ticket id is kept in the URL hash, so a reload reopens it, and changing the hash opens that ticket.
- Colours do not animate when the system theme changes. Only hover changes are transitioned.
- No request leaves localhost. No library, no build step, one file.

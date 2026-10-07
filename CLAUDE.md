# CLAUDE.md — instructions for Claude Code working on pocket astro

This file has the same rules as `AGENTS.md`, plus a Claude-specific
section at the end. If you change a shared rule, change it in both files.

## What this project is

Pocket astro is an offline pocket astrologer for the Nokia N810. It shows a
birth chart with descriptions of each placement, tracks planet positions and
retrogrades, shows the moon phase, explains houses and aspects, and keeps a
reflection journal. It is a semester project for PSAM 5600 (Parsons, Fall 2026).

## The two machines

| | Device: Nokia N810 | Server: Oracle Cloud node |
|---|---|---|
| OS | Maemo OS2008 (Debian-based), kernel 2.6.21 | Ubuntu 24.04, arm64 |
| Hardware | ARMv6 ~400 MHz, 128 MB RAM | 4 CPUs, 24 GB RAM |
| Shell | BusyBox v1.6.1 `ash` (strict POSIX `sh`) | bash |
| Code lives in | `device/` | `server/` |

Do the heavy work (computing planet positions, moon phases, LLM calls,
modern HTTPS) on the server. The N810 shows results and must stay fast.

- The app should work with no network once its data is on the device.
  The server produces data files (for example, precomputed positions for the
  coming months) that are copied to the N810, rather than the N810 asking
  the server for data while you use it.

## The interface is graphical, and the route is not decided

The app has a real graphical interface, not a terminal one. Two routes are
still open:

1. Offline HTML pages with simple JavaScript, opened in the N810's built-in
   browser (MicroB, an old Gecko engine).
2. A native Hildon app in Python/PyGTK. OS2008 ships Python 2.5;
   check this on the device before relying on it.

**Do not pick a route on your own.** If a task depends on the choice, stop and
ask. Whichever route is chosen, assume old engines: no modern JS syntax, no
build tools, no frameworks that need a recent runtime.

## Rules for code on the N810

- Shell scripts must be strict POSIX `sh` for BusyBox 1.6.1: no `[[ ]]`, no
  `${var:i:1}`, no `for ((…))`, no fractional `sleep`.
- Keep memory and CPU use small. Avoid anything that has to load more
  than a few MB into memory at once.
- Don't assume the N810 can talk to modern HTTPS sites; its TLS is too old.

## Private data

- Real birth details go in `data/private/`, and secrets (API keys) go in
  `.env`. Both are in `.gitignore`. Never commit them, never copy them into
  examples, tests or docs, and never print them in logs.
- Use made-up birth data for examples and tests.
- Ask before sending real birth data to any outside LLM API.

## Astrology content

- Tropical zodiac and Placidus houses, unless told otherwise.
- Placement descriptions should invite reflection ("you may notice…")
  rather than make predictions or claims about the user's fate.
- Reference text (placements, houses, aspects) lives in `data/`.

## What you may do without asking

- Small fixes inside one file: typos, obvious bugs, renaming, comments.
- Reading files and running read-only commands.

## What needs the user's OK first

- New features, new files or folders, or changes that touch several files.
- Adding any dependency or installing anything.
- Commits, pushes, branches and pull requests.
- Anything that runs on, copies to or changes the N810.
- Deleting files, or changes to `.gitignore`, `AGENTS.md` or `CLAUDE.md`.

When you ask, say what you plan to do and why, in plain language.

## Git and attribution

- Every commit you help make ends with a `Co-Authored-By:` trailer naming the
  specific model (for example `Co-Authored-By: Claude Opus 5.5
  <noreply@anthropic.com>`). This is course policy and is graded.
- Commit messages describe what changed and why, in a sentence or two.
- Use a branch and a pull request for major changes.
- This repo uses a repo-local git identity. Don't change it.
- Never commit to the class repo (`mfadt/sld-fall-2026`) from here.

## Checking your work

- TBD in Week 9 (telemetry and testing). For now, explain how the user can
  check each change by hand, on the server and on the N810.

## Claude Code specifics

- Explain each command in a sentence before you run it, and go one step at a
  time. The user is learning, and directing you is part of their grade.
- When something fails, ask for (or show) the exact error text instead of
  guessing.
- For anything on the "needs the user's OK" list, use plan mode and lay
  out the plan before editing.
- Name the model you actually are in the `Co-Authored-By:` trailer. Don't copy
  the example name if you are a different model.
- Don't save anything from `data/private/` or `.env` to memory.

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

- The app's pages live on the N810 and open without a network.
- The birth chart is the exception. A form on the N810 sends birth details
  to the server over plain HTTP when Wi-Fi is on. The server calculates the
  chart with Swiss Ephemeris (`pyswisseph`) and sends it back as a page the
  N810 can show. If the server can't be reached, the form must say so
  clearly instead of failing silently.
- Plain HTTP, not HTTPS, because the N810's TLS is too old for modern HTTPS.

## The interface: offline HTML in the N810's browser

Decided on 2026-10-21. The app is a set of HTML pages with simple JavaScript,
opened in the N810's built-in browser (MicroB, an old Gecko engine). The user
opens it from a "Web shortcut" applet on the home screen.

- There is no Python on the N810 (checked 2026-10-21). Nothing written in
  Python runs on the device; Python belongs in `server/`.
- There is no root on the N810 (it would need R&D mode, which is not
  enabled). Don't plan anything that needs root, such as an app-menu launcher.
- Assume an old engine: no modern JS syntax (no `let`, `const`, arrow
  functions, `fetch` or promises), no build tools, no frameworks.
- A page working in a modern browser proves nothing. It has to be checked in
  MicroB on the N810.

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
- Birth details sent from the N810 travel unencrypted. The server must not
  log them or keep them after it has answered the request.

## Astrology content

- Tropical zodiac and Placidus houses, calculated with Swiss Ephemeris.
- Placement descriptions should invite reflection ("you may notice…")
  rather than make predictions or claims about the user's fate.
- Reference text (placements, houses, aspects) lives in `data/`.

## License

The project is AGPL-3.0, because it uses Swiss Ephemeris (`pyswisseph`),
which is AGPL. AGPL's network rule applies: the server is a service people
use, so its source must stay public in this repo. Ask before adding any
dependency, and check that its license is compatible with AGPL.

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

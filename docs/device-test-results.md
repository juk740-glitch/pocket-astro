# N810 device test results (2026-11-18)

What the Nokia N810 can actually do, checked on the device. These results
decided the interface route: offline HTML pages in the built-in browser.

## Software on the device

| Check | Command or method | Result |
|---|---|---|
| Python | `python -V` in X Terminal | Not installed ("python not found") |
| BusyBox web server | `busybox httpd -h` | Not included ("httpd not found") |
| SSH server | installed `openssh` 4.7 from the archival catalogue (see below) | Works; a Mac can connect |

Without Python, the PyGTK route would mean finding and installing 2008-era
packages first. Without a web server, the device can't serve pages to itself.
Both were dropped in favour of plain HTML files.

## The browser (MicroB)

Engine string:

```
Mozilla/5.0 (X11; U; Linux armv6l; en-US; rv:1.9a6pre) Gecko/20080828 Firefox/3.0a1 Tablet browser 0.3.7
```

That is a **pre-release Gecko 1.9** (the engine behind Firefox 3), from 2008.

Results from [`device/feature-test.html`](../device/feature-test.html), opened
from a file (`file:///home/user/MyDocs/feature-test.html`):

| Feature | Result | What it means for Pocket Astro |
|---|---|---|
| Cookies | YES | The only way to save journal entries in the browser |
| localStorage | NO | |
| globalStorage | NO | |
| sessionStorage | NO | |
| Built-in JSON reader | NO | Server writes data as `.js` files instead of `.json` |
| Read a file next to the page | YES | Pages can load local data files |
| Canvas drawing | YES | The chart wheel can be drawn |
| Text on canvas | NO | Labels go in HTML on top of the canvas, or in images |
| SVG | NO | Use canvas or images |
| Astrology symbols in fonts | Only ☉ ♂ ♀ | All other symbols must be images made by the server |
| See-through colours | Inconclusive | The test had nothing behind the strip; needs a better test |

## Still to check

- **Do cookies survive closing the browser and restarting the N810?** The
  counter reached 2 after a reload; a full browser restart and a reboot
  haven't been confirmed yet.
- How much text fits in cookies before the browser drops some (each cookie
  holds about 4 KB).
- Rounded corners, and a better see-through test.

## How files get to the N810

The cloud server can't reach the N810 directly (the N810 is on a home or
school Wi-Fi network). Files go **server → Mac → N810**:

1. Mac: `scp ubuntu@<server>:~/pocket-astro/device/<file> .`
2. Mac: `scp -O -o HostKeyAlgorithms=+ssh-rsa -o KexAlgorithms=+diffie-hellman-group14-sha1 <file> root@<n810-ip>:/home/user/MyDocs/`
3. N810 browser: `file:///home/user/MyDocs/<file>`

The extra `-O` and `-o` options are needed because the N810's SSH is from 2007.

The software catalogue that provided `openssh` (Application manager → Tools →
Application catalogue → New):

| Field | Value |
|---|---|
| Web address | `http://maemo.viniciuspaes.com/extras/` |
| Distribution | `diablo` |
| Components | `free non-free` |

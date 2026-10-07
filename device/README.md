# device/

Code that runs on the Nokia N810 (Maemo OS2008, BusyBox v1.6.1 `ash`).

Scripts here must be strict POSIX `sh`: no `[[ ]]`, no `${var:i:1}`,
no `for ((…))`, and no fractional `sleep`. Keep them lightweight — the
N810 has a ~400 MHz CPU and 128 MB of RAM.

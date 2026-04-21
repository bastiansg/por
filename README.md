# P.O.R (Pop Oracle Robot)

## Setup (work in progress)

### Qdrant

To run qdrant on the raspberry pi 5, append `kernel=kernel8.img` to `/boot/firmware/config.txt` and reboot; this changes the kernel page size to 4k.

### Static IP

```bash
$ nmcli device status
$ sudo nmtui edit "Wired connection 1"
```

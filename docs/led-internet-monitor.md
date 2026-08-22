# Internet LED Monitor

The JIDU6811/JIDU6J11 image includes a supervised OpenWrt service that maps the active Internet connection to the three status LEDs.

| Condition | LED indication |
| --- | --- |
| Network is still settling during boot | Red blinking |
| No usable route or Internet is unreachable | Red solid |
| Internet is reachable through the logical `wan` interface | Green solid |
| Internet is reachable through USB tethering on `usb0` | Red + blue solid (magenta/pink) |

Pink is produced electrically by combining the red and blue channels. The exact perceived color depends on the LED diffuser.

## How the monitor decides the state

The monitor first asks the kernel which interface it would use to reach `1.1.1.1` with `ip -4 route get`. This makes the routing table authoritative when both WAN and USB tethering are connected. It does not select USB merely because `usb0` exists.

For a route identified as USB, the monitor checks connectivity through `usb0`. For a route identified as WAN, it resolves the logical `wan` interface’s actual Layer 3 device through ubus and checks connectivity through that device. An unfamiliar or unavailable route is treated as unknown rather than being incorrectly labelled WAN or USB.

A state change requires two consecutive successful or failed checks by default. This prevents a single lost packet from changing the LED indication. The values are configurable at the top of `files/usr/bin/led_internet_monitor.sh`:

| Setting | Default | Purpose |
| --- | ---: | --- |
| `WAN_INTERFACE` | `wan` | Logical OpenWrt WAN interface |
| `USB_DEVICE` | `usb0` | Linux device used by USB tethering |
| `PING_TARGET` | `1.1.1.1` | Connectivity-check destination |
| `PING_TIMEOUT` | `2` | Timeout for each ping, in seconds |
| `REQUIRED_SUCCESS` | `2` | Successful checks before an online state |
| `REQUIRED_FAILURE` | `2` | Failed checks before the offline state |
| `CHECK_INTERVAL` | `5` | Seconds between checks |
| `BOOT_TIMEOUT` | `60` | Maximum time to retain the boot indication |

## Included files

The firmware installs the following files:

```text
/usr/bin/led_internet_monitor.sh
/etc/init.d/led_internet_monitor
```

The monitor controls the LED class devices exported by the device tree:

```text
/sys/class/leds/red:status
/sys/class/leds/green:status
/sys/class/leds/blue:status
```

It selects the `none` trigger before setting a solid state and uses the kernel `timer` trigger for the boot blink. On shutdown, all three LEDs are turned off. If the required LED devices are absent, the monitor logs an error and exits instead of silently claiming a state.

## Service management

The image enables the service from `files/etc/uci-defaults/99-jidu6811-setup`. To inspect or control it on a running router:

```sh
/etc/init.d/led_internet_monitor status
/etc/init.d/led_internet_monitor restart
/etc/init.d/led_internet_monitor enable
/etc/init.d/led_internet_monitor disable
```

The service uses OpenWrt’s normal `procd` supervision. If the monitor exits unexpectedly, `procd` restarts it after a five-second initial delay with a bounded retry window. Logs are available with:

```sh
logread | grep internet-led
```

## Installation and verification on an existing router

The preferred installation method is to build and flash the firmware image so the files and first-boot setup are installed together. If the repository is available on the router, the included helper installs the two files and enables the service:

```sh
./scripts/install-led-internet-monitor.sh
```

The helper refuses non-OpenWrt roots and must be run as root. It also accepts a staging root as its first argument; service enablement is performed after that root boots. For a manual test of files copied to a running router, use:

```sh
chmod 755 /usr/bin/led_internet_monitor.sh
chmod 755 /etc/init.d/led_internet_monitor
/usr/bin/led_internet_monitor.sh &
```

Allow at least 10–15 seconds for the consecutive checks to settle, then stop the foreground test before starting the supervised service:

```sh
killall led_internet_monitor.sh
/etc/init.d/led_internet_monitor enable
/etc/init.d/led_internet_monitor start
```

Verify the actual tethering device and WAN device before troubleshooting LED colors:

```sh
ubus call network.interface.wan_usb status
ubus call network.interface.wan status
ip -4 route get 1.1.1.1
```

If the USB interface is not `usb0`, change `USB_DEVICE` in the monitor script and ensure the matching OpenWrt network interface is configured. The service follows the kernel’s selected route, so the LED color should change automatically when the default route moves between WAN and USB tethering.

## Avoiding competing LED configuration

Only one service should control these LEDs. Check for system LED entries before adding another LED configuration:

```sh
uci show system | grep -E 'red:status|green:status|blue:status'
```

If another enabled LED service assigns a trigger to any of these devices, remove or disable that competing assignment. The monitor itself clears the trigger before applying solid colors, but a separate daemon can still race it and produce inconsistent indications.

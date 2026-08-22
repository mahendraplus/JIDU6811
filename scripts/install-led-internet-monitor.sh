#!/bin/sh
# Install the Internet LED monitor into a running OpenWrt system.
# Usage: ./scripts/install-led-internet-monitor.sh [target-root]

set -u

ROOT="${1:-/}"
SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
REPO_ROOT="$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)"

fail()
{
    echo "install-led-internet-monitor: $*" >&2
    exit 1
}

[ "$(id -u)" -eq 0 ] || fail "must run as root"
[ -f "$ROOT/etc/rc.common" ] ||
    fail "target does not look like OpenWrt: missing $ROOT/etc/rc.common"

mkdir -p "$ROOT/usr/bin" "$ROOT/etc/init.d"
cp "$REPO_ROOT/files/usr/bin/led_internet_monitor.sh" \
    "$ROOT/usr/bin/led_internet_monitor.sh"
cp "$REPO_ROOT/files/etc/init.d/led_internet_monitor" \
    "$ROOT/etc/init.d/led_internet_monitor"
chmod 755 "$ROOT/usr/bin/led_internet_monitor.sh" \
    "$ROOT/etc/init.d/led_internet_monitor"

if [ "$ROOT" = "/" ]; then
    /etc/init.d/led_internet_monitor enable
    /etc/init.d/led_internet_monitor restart 2>/dev/null ||
        /etc/init.d/led_internet_monitor start
    echo "Internet LED monitor installed and started."
else
    echo "Internet LED monitor installed into $ROOT."
    echo "Enable it after boot with: /etc/init.d/led_internet_monitor enable"
fi

#!/bin/sh
# LED Internet Monitor for JIDU6811 / JIDU6J11
#
# LED states:
#   booting       red blinking
#   offline       red solid
#   WAN internet  green solid
#   USB internet  red + blue (magenta/pink) solid
#
# The default route is authoritative for uplink selection. Connectivity is
# then checked through the device selected by that route.

PATH="${PATH:-/usr/sbin:/usr/bin:/sbin:/bin}"

# ---------------------------------------------------------------------------
# Configuration. Values may be overridden in the environment for diagnostics.
# ---------------------------------------------------------------------------

WAN_INTERFACE="${WAN_INTERFACE:-wan}"
USB_DEVICE="${USB_DEVICE:-usb0}"
PING_TARGET="${PING_TARGET:-1.1.1.1}"
PING_TIMEOUT="${PING_TIMEOUT:-2}"
REQUIRED_SUCCESS="${REQUIRED_SUCCESS:-2}"
REQUIRED_FAILURE="${REQUIRED_FAILURE:-2}"
CHECK_INTERVAL="${CHECK_INTERVAL:-5}"
BOOT_TIMEOUT="${BOOT_TIMEOUT:-60}"

LED_RED="${LED_RED:-/sys/class/leds/red:status}"
LED_GREEN="${LED_GREEN:-/sys/class/leds/green:status}"
LED_BLUE="${LED_BLUE:-/sys/class/leds/blue:status}"

log_msg()
{
    logger -t internet-led "$*"
}

led_exists()
{
    [ -d "$1" ] && [ -f "$1/brightness" ]
}

if ! led_exists "$LED_RED" ||
   ! led_exists "$LED_GREEN" ||
   ! led_exists "$LED_BLUE"; then
    log_msg "ERROR: Required RGB LEDs are missing"
    exit 1
fi

# ---------------------------------------------------------------------------
# Low-level LED operations
# ---------------------------------------------------------------------------

led_trigger_none()
{
    local led="$1"

    if [ -f "$led/trigger" ]; then
        echo none > "$led/trigger" 2>/dev/null || true
    fi
}

led_off()
{
    local led="$1"

    led_trigger_none "$led"
    echo 0 > "$led/brightness" 2>/dev/null || true
}

led_on()
{
    local led="$1"

    led_trigger_none "$led"
    echo 1 > "$led/brightness" 2>/dev/null || true
}

all_off()
{
    led_off "$LED_RED"
    led_off "$LED_GREEN"
    led_off "$LED_BLUE"
}

set_boot()
{
    # The kernel timer trigger provides a reliable blink without a second
    # userspace loop competing with the monitor.
    led_off "$LED_GREEN"
    led_off "$LED_BLUE"

    if [ -f "$LED_RED/trigger" ]; then
        echo timer > "$LED_RED/trigger" 2>/dev/null || true
        [ -f "$LED_RED/delay_on" ] &&
            echo 500 > "$LED_RED/delay_on" 2>/dev/null || true
        [ -f "$LED_RED/delay_off" ] &&
            echo 500 > "$LED_RED/delay_off" 2>/dev/null || true
    else
        led_on "$LED_RED"
    fi
}

set_red()
{
    all_off
    led_on "$LED_RED"
}

set_green()
{
    all_off
    led_on "$LED_GREEN"
}

set_pink()
{
    all_off
    # Red + blue is electrically magenta and is perceived as pink on some
    # diffusers.
    led_on "$LED_RED"
    led_on "$LED_BLUE"
}

# ---------------------------------------------------------------------------
# Uplink and connectivity checks
# ---------------------------------------------------------------------------

get_wan_device()
{
    local dev

    dev="$(ubus call "network.interface.$WAN_INTERFACE" status 2>/dev/null |
        jsonfilter -e '@.l3_device' 2>/dev/null)"

    [ -n "$dev" ] && echo "$dev"
}

get_route_device()
{
    local route
    local dev

    route="$(ip -4 route get "$PING_TARGET" 2>/dev/null)"
    [ -n "$route" ] || return 1

    dev="$(echo "$route" |
        sed -n 's/.* dev \([^ ]*\).*/\1/p' |
        awk '{print $1}')"

    [ -n "$dev" ] && echo "$dev"
}

check_internet()
{
    local dev="$1"

    [ -n "$dev" ] || return 1

    ping -4 -c 2 -W "$PING_TIMEOUT" -I "$dev" \
        "$PING_TARGET" >/dev/null 2>&1
}

classify_uplink()
{
    local route_dev
    local wan_dev

    route_dev="$(get_route_device)"
    [ -n "$route_dev" ] || {
        echo UNKNOWN
        return 0
    }

    if [ "$route_dev" = "$USB_DEVICE" ]; then
        echo USB
        return 0
    fi

    wan_dev="$(get_wan_device)"
    if [ -n "$wan_dev" ] && [ "$route_dev" = "$wan_dev" ]; then
        echo WAN
        return 0
    fi

    # Some configurations expose the logical interface name in route output.
    if [ "$route_dev" = "$WAN_INTERFACE" ]; then
        echo WAN
        return 0
    fi

    echo UNKNOWN
}

# ---------------------------------------------------------------------------
# State transitions and cleanup
# ---------------------------------------------------------------------------

cleanup()
{
    all_off
}

stop_monitor()
{
    cleanup
    exit 0
}

trap stop_monitor TERM INT
trap cleanup EXIT

log_msg "Starting Internet LED monitor"
all_off
set_boot

START_TIME="$(date +%s)"
SUCCESS_COUNT=0
FAILURE_COUNT=0
LAST_STATE="BOOT"
LAST_UPLINK=""

set_offline()
{
    FAILURE_COUNT=$((FAILURE_COUNT + 1))
    SUCCESS_COUNT=0

    if [ "$FAILURE_COUNT" -ge "$REQUIRED_FAILURE" ] &&
       [ "$LAST_STATE" != "OFFLINE" ]; then
        log_msg "No usable Internet route or selected uplink is unreachable"
        set_red
        LAST_STATE="OFFLINE"
    fi
}

while :; do
    NOW="$(date +%s)"
    BOOT_ELAPSED=$((NOW - START_TIME))
    UPLINK="$(classify_uplink)"

    # Do not carry success/failure samples across a WAN-to-USB transition.
    if [ "$UPLINK" != "$LAST_UPLINK" ]; then
        SUCCESS_COUNT=0
        FAILURE_COUNT=0
        LAST_UPLINK="$UPLINK"
    fi

    case "$UPLINK" in
        WAN)
            WAN_DEV="$(get_wan_device)"
            if [ -n "$WAN_DEV" ] && check_internet "$WAN_DEV"; then
                SUCCESS_COUNT=$((SUCCESS_COUNT + 1))
                FAILURE_COUNT=0
                if [ "$SUCCESS_COUNT" -ge "$REQUIRED_SUCCESS" ] &&
                   [ "$LAST_STATE" != "WAN" ]; then
                    log_msg "Internet available via WAN ($WAN_DEV)"
                    set_green
                    LAST_STATE="WAN"
                fi
            else
                set_offline
            fi
            ;;

        USB)
            if check_internet "$USB_DEVICE"; then
                SUCCESS_COUNT=$((SUCCESS_COUNT + 1))
                FAILURE_COUNT=0
                if [ "$SUCCESS_COUNT" -ge "$REQUIRED_SUCCESS" ] &&
                   [ "$LAST_STATE" != "USB" ]; then
                    log_msg "Internet available via USB tethering ($USB_DEVICE)"
                    set_pink
                    LAST_STATE="USB"
                fi
            else
                set_offline
            fi
            ;;

        UNKNOWN|*)
            SUCCESS_COUNT=0
            FAILURE_COUNT=$((FAILURE_COUNT + 1))

            # During early boot, keep the informative boot indication instead
            # of reporting an outage before network routing has settled.
            if [ "$BOOT_ELAPSED" -lt "$BOOT_TIMEOUT" ]; then
                if [ "$LAST_STATE" != "BOOT" ]; then
                    log_msg "Waiting for network routing"
                    set_boot
                    LAST_STATE="BOOT"
                fi
            elif [ "$LAST_STATE" != "OFFLINE" ]; then
                log_msg "No usable Internet route"
                set_red
                LAST_STATE="OFFLINE"
            fi
            ;;
    esac

    sleep "$CHECK_INTERVAL"
done

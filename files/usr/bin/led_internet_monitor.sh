#!/bin/sh
# LED Internet Monitor for JIDU6811 / JIDU6J11
# Monitors real internet connectivity and controls status LEDs
# Green = Online / Internet OK, Blue = Searching / Connecting, Red = Offline / No WAN

find_led_path() {
    local color="$1"
    for p in /sys/class/leds/*${color}*/brightness /sys/class/leds/led-${color}/brightness /sys/class/leds/${color}:status/brightness; do
        if [ -f "$p" ]; then
            echo "$p"
            return 0
        fi
    done
    return 1
}

LED_GREEN=$(find_led_path "green")
LED_BLUE=$(find_led_path "blue")
LED_RED=$(find_led_path "red")

set_led() {
    local target="$1"
    local val="$2"
    [ -n "$target" ] && [ -w "$target" ] && echo "$val" > "$target" 2>/dev/null
}

led_off() {
    set_led "$LED_GREEN" 0
    set_led "$LED_BLUE" 0
    set_led "$LED_RED" 0
}

led_green() {
    set_led "$LED_GREEN" 1
    set_led "$LED_BLUE" 0
    set_led "$LED_RED" 0
}

led_blue() {
    set_led "$LED_GREEN" 0
    set_led "$LED_BLUE" 1
    set_led "$LED_RED" 0
}

led_red() {
    set_led "$LED_GREEN" 0
    set_led "$LED_BLUE" 0
    set_led "$LED_RED" 1
}

check_connectivity() {
    # 1. First test public DNS resolvers
    if ping -c 1 -W 2 1.1.1.1 >/dev/null 2>&1 || ping -c 1 -W 2 8.8.8.8 >/dev/null 2>&1; then
        return 0
    fi

    # 2. Check if default WAN gateway responds
    local def_gw
    def_gw=$(ip -4 route show default 2>/dev/null | awk '/default/ {print $3}' | head -n 1)
    if [ -n "$def_gw" ] && [ "$def_gw" != "127.0.0.1" ] && [ "$def_gw" != "192.168.1.1" ]; then
        if ping -c 1 -W 2 "$def_gw" >/dev/null 2>&1; then
            return 0
        fi
    fi

    return 1
}

FAIL_COUNT=0
MAX_FAIL=3

# Initial state: Blue (connecting/searching)
led_blue

while true; do
    # Re-evaluate LED paths if not found at initial start
    [ -z "$LED_GREEN" ] && LED_GREEN=$(find_led_path "green")
    [ -z "$LED_BLUE" ] && LED_BLUE=$(find_led_path "blue")
    [ -z "$LED_RED" ] && LED_RED=$(find_led_path "red")

    if check_connectivity; then
        FAIL_COUNT=0
        led_green
    else
        FAIL_COUNT=$((FAIL_COUNT + 1))
        if [ "$FAIL_COUNT" -ge "$MAX_FAIL" ]; then
            led_red
        else
            led_blue
        fi
    fi
    sleep 5
done

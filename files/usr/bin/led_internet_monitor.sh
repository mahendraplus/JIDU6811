#!/bin/sh
# LED Internet Monitor for JIDU6811
# Monitors internet connectivity and controls status LEDs
# Green = internet OK, Blue = searching, Red = no internet

GATEWAY="192.168.1.1"
LED_GREEN="/sys/class/leds/led-green/brightness"
LED_BLUE="/sys/class/leds/led-blue/brightness"
LED_RED="/sys/class/leds/led-red/brightness"

led_off() {
    echo 0 > "$LED_GREEN" 2>/dev/null
    echo 0 > "$LED_BLUE" 2>/dev/null
    echo 0 > "$LED_RED" 2>/dev/null
}

led_green() {
    echo 1 > "$LED_GREEN" 2>/dev/null
    echo 0 > "$LED_BLUE" 2>/dev/null
    echo 0 > "$LED_RED" 2>/dev/null
}

led_blue() {
    echo 0 > "$LED_GREEN" 2>/dev/null
    echo 1 > "$LED_BLUE" 2>/dev/null
    echo 0 > "$LED_RED" 2>/dev/null
}

led_red() {
    echo 0 > "$LED_GREEN" 2>/dev/null
    echo 0 > "$LED_BLUE" 2>/dev/null
    echo 1 > "$LED_RED" 2>/dev/null
}

FAIL_COUNT=0
MAX_FAIL=3

while true; do
    if ping -c 1 -W 2 "$GATEWAY" >/dev/null 2>&1; then
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

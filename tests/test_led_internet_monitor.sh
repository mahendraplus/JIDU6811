#!/usr/bin/env bash
set -u

ROOT="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
MONITOR="$ROOT/files/usr/bin/led_internet_monitor.sh"
TEST_ROOT="$(mktemp -d)"
trap 'rm -rf "$TEST_ROOT"' EXIT

fail()
{
    echo "FAIL: $*" >&2
    exit 1
}

assert_snapshot()
{
    expected="$1"
    actual="$(cat "$TEST_ROOT/snapshot")"
    [ "$actual" = "$expected" ] || fail "expected $expected, got $actual"
}

run_case()
{
    name="$1"
    route="$2"
    ping_ok="$3"
    boot_timeout="$4"
    loops="$5"
    expected="$6"

    case_dir="$TEST_ROOT/$name"
    mkdir -p "$case_dir/bin" "$case_dir/leds" \
        "$case_dir/leds/red:status" "$case_dir/leds/green:status" \
        "$case_dir/leds/blue:status"
    for color in red green blue; do
        printf '0\n' > "$case_dir/leds/$color:status/brightness"
        printf 'none\n' > "$case_dir/leds/$color:status/trigger"
        printf '500\n' > "$case_dir/leds/$color:status/delay_on"
        printf '500\n' > "$case_dir/leds/$color:status/delay_off"
    done

    cat > "$case_dir/bin/ip" <<'EOF'
#!/bin/sh
printf '1.1.1.1 via 192.0.2.1 dev %s src 192.0.2.2\n' "$TEST_ROUTE"
EOF
    cat > "$case_dir/bin/ubus" <<'EOF'
#!/bin/sh
printf '{}\n'
EOF
    cat > "$case_dir/bin/jsonfilter" <<'EOF'
#!/bin/sh
printf 'eth0\n'
EOF
    cat > "$case_dir/bin/ping" <<'EOF'
#!/bin/sh
exit "$TEST_PING_OK"
EOF
    cat > "$case_dir/bin/logger" <<'EOF'
#!/bin/sh
printf '%s\n' "$*" >> "$TEST_LOG"
EOF
    cat > "$case_dir/bin/sleep" <<'EOF'
#!/bin/sh
count=0
[ -f "$TEST_SLEEP_COUNT" ] && count="$(cat "$TEST_SLEEP_COUNT")"
count=$((count + 1))
printf '%s\n' "$count" > "$TEST_SLEEP_COUNT"
if [ "$count" -ge "$TEST_LOOPS" ]; then
    {
        for color in red green blue; do
            printf '%s=' "$color"
            cat "$TEST_LED_ROOT/$color:status/brightness"
        done
    } > "$TEST_SNAPSHOT"
    kill -TERM "$PPID"
fi
/usr/bin/sleep 0.01
EOF
    chmod 755 "$case_dir/bin"/*

    TEST_ROUTE="$route" \
    TEST_PING_OK="$ping_ok" \
    TEST_LOOPS="$loops" \
    TEST_LED_ROOT="$case_dir/leds" \
    TEST_SLEEP_COUNT="$case_dir/sleep.count" \
    TEST_SNAPSHOT="$TEST_ROOT/snapshot" \
    TEST_LOG="$case_dir/log" \
    PATH="$case_dir/bin:/usr/sbin:/usr/bin:/sbin:/bin" \
    LED_RED="$case_dir/leds/red:status" \
    LED_GREEN="$case_dir/leds/green:status" \
    LED_BLUE="$case_dir/leds/blue:status" \
    BOOT_TIMEOUT="$boot_timeout" \
    REQUIRED_SUCCESS=2 \
    REQUIRED_FAILURE=2 \
    CHECK_INTERVAL=1 \
    "$MONITOR" >/dev/null 2>&1 || true

    assert_snapshot "$expected"
    echo "PASS: $name"
}

run_case wan eth0 0 0 2 'red=0
green=1
blue=0'
run_case usb usb0 0 0 2 'red=1
green=0
blue=1'
run_case offline eth0 1 0 2 'red=1
green=0
blue=0'
run_case boot unknown 1 60 1 'red=0
green=0
blue=0'

echo "All LED monitor behavioral tests passed."

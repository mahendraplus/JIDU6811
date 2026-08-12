#!/usr/bin/env python3
"""Splits a sysupgrade.bin into kernel.bin and rootfs.bin for ubinize"""
import sys

with open(sys.argv[1], 'rb') as f:
    data = f.read()

idx = data.find(b'hsqs')
if idx < 0:
    print('ERROR: squashfs magic not found')
    sys.exit(1)

open('kernel.bin', 'wb').write(data[:idx])
open('rootfs.bin', 'wb').write(data[idx:])
print(f'kernel={idx}B rootfs={len(data)-idx}B')

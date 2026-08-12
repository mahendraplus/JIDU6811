#!/usr/bin/env python3
"""Appends the jio_jidu6811 device profile to ipq95xx.mk"""
import sys, textwrap

mk = sys.argv[1]

block = textwrap.dedent("""\

    define Device/jio_jidu6811
    \t$(call Device/FitImage)
    \t$(call Device/UbiFit)
    \tDEVICE_VENDOR := Jio
    \tDEVICE_MODEL := JIDU6811
    \tDEVICE_DTS := ipq9574-jidu6811
    \tSOC := ipq9574
    \tBLOCKSIZE := 128k
    \tPAGESIZE := 2048
    \tDEVICE_PACKAGES := kmod-ath11k-ahb kmod-ath11k kmod-ath11k-pci \\
    \t\tath11k-firmware-ipq9574 ath11k-firmware-qcn9074 \\
    \t\twpad-basic-mbedtls iwinfo wireless-regdb \\
    \t\tkmod-usb3 kmod-usb-dwc3 kmod-usb-dwc3-qcom \\
    \t\tkmod-leds-gpio kmod-gpio-button-hotplug kmod-ledtrig-netdev \\
    \t\tkmod-qcom-ppe uboot-envtools luci
    \tIMAGE/sysupgrade.bin := sysupgrade-tar | append-metadata
    endef
    TARGET_DEVICES += jio_jidu6811
""")

with open(mk, 'a') as f:
    f.write(block)

print("Device profile appended to", mk)

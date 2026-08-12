#!/usr/bin/env python3
"""Appends Sandiep JIDU6J11 device profiles to ipq95xx.mk"""
import sys, textwrap

mk = sys.argv[1]

block = textwrap.dedent("""\

    define Device/jiorouter_ax6000-jidu6j11
    \t$(call Device/FitImage)
    \t$(call Device/UbiFit)
    \tDEVICE_VENDOR := JioRouter
    \tDEVICE_MODEL := AX6000
    \tSOC := ipq9554
    \tBLOCKSIZE := 128k
    \tPAGESIZE := 2048
    \tDEVICE_PACKAGES := kmod-ath11k-ahb kmod-ath11k kmod-ath11k-pci \\
    \t\tath11k-firmware-ipq9574 ath11k-firmware-qcn9074 \\
    \t\tuboot-envtools kmod-leds-gpio kmod-gpio-button-hotplug \\
    \t\tkmod-qcom-ppe kmod-usb3 kmod-usb-dwc3 kmod-usb-dwc3-qcom \\
    \t\tkmod-ledtrig-netdev
    endef

    define Device/jiorouter_ax6000-jidu6j11-6811
    \t$(call Device/jiorouter_ax6000-jidu6j11)
    \tDEVICE_VARIANT := JIDU6J11-6811
    \tDEVICE_DTS := ipq9554-jiorouter-ax6000-jidu6j11-6811
    endef
    TARGET_DEVICES += jiorouter_ax6000-jidu6j11-6811

    define Device/jio_jidu6811
    \t$(call Device/jiorouter_ax6000-jidu6j11)
    \tDEVICE_VENDOR := Jio
    \tDEVICE_MODEL := JIDU6811
    \tDEVICE_DTS := ipq9574-jidu6811
    endef
    TARGET_DEVICES += jio_jidu6811
""")

with open(mk, 'a') as f:
    f.write(block)

print("Device profiles appended to", mk)

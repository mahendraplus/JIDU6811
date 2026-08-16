#!/usr/bin/env python3
"""Appends JIDU6811 device profiles to ipq95xx.mk"""
import sys

mk = sys.argv[1]

block = """
define Device/jiorouter_ax6000-jidu6j11
\t$(call Device/FitImage)
\t$(call Device/UbiFit)
\tDEVICE_VENDOR := JioRouter
\tDEVICE_MODEL := AX6000
\tSOC := ipq9554
\tBLOCKSIZE := 128k
\tPAGESIZE := 2048
\tSUPPORTED_DEVICES := jio,jidu6811 jiorouter,ax6000-jidu6j11-6811 jiorouter,ax6000-jidu6j11
\tDEVICE_PACKAGES := kmod-ath11k-ahb kmod-ath11k kmod-ath11k-pci \\
\t\tuboot-envtools kmod-leds-gpio kmod-gpio-button-hotplug \\
\t\tkmod-qcom-ppe kmod-usb3 kmod-usb-dwc3 kmod-usb-dwc3-qcom \\
\t\tkmod-ledtrig-netdev ath11k-firmware-ipq9574 ath11k-firmware-qcn9074
endef

define Device/jiorouter_ax6000-jidu6j11-6811
\t$(call Device/jiorouter_ax6000-jidu6j11)
\tDEVICE_VARIANT := JIDU6J11-6811
\tDEVICE_DTS := ipq9554-jiorouter-ax6000-jidu6j11-6811
\tSUPPORTED_DEVICES := jiorouter,ax6000-jidu6j11-6811 jiorouter,ax6000-jidu6j11 jio,jidu6811
endef
TARGET_DEVICES += jiorouter_ax6000-jidu6j11-6811

define Device/jio_jidu6811
\t$(call Device/jiorouter_ax6000-jidu6j11)
\tDEVICE_VENDOR := Jio
\tDEVICE_MODEL := JIDU6811
\tDEVICE_DTS := ipq9574-jidu6811
\tSUPPORTED_DEVICES := jio,jidu6811 jiorouter,ax6000-jidu6j11-6811 jiorouter,ax6000-jidu6j11
endef
TARGET_DEVICES += jio_jidu6811
"""

with open(mk, 'a') as f:
    f.write(block)

print("Device profiles appended to", mk)

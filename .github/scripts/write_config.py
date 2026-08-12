#!/usr/bin/env python3
"""Writes OpenWrt .config for jio_jidu6811 build"""
import sys

config = [
    "CONFIG_TARGET_qualcommbe=y",
    "CONFIG_TARGET_qualcommbe_ipq95xx=y",
    "CONFIG_TARGET_qualcommbe_ipq95xx_DEVICE_jio_jidu6811=y",
    "CONFIG_TARGET_ROOTFS_INITRAMFS=y",
    "CONFIG_TARGET_INITRAMFS_FORCE=y",
    "CONFIG_KERNEL_GZIP=y",
    "CONFIG_CCACHE=y",

    # Core Qualcomm IPQ9574 drivers built-in (=y)
    "CONFIG_PACKAGE_kmod-qcom-gcc-ipq9574=y",
    "CONFIG_PACKAGE_kmod-qcom-nsscc-ipq9574=y",
    "CONFIG_PACKAGE_kmod-qcom-ppe=y",

    # Wi-Fi & Wireless stack built-in (=y)
    "CONFIG_PACKAGE_kmod-ath11k=y",
    "CONFIG_PACKAGE_kmod-ath11k-pci=y",
    "CONFIG_PACKAGE_kmod-ath11k-ahb=y",
    "CONFIG_PACKAGE_wpad-basic-mbedtls=y",
    "CONFIG_PACKAGE_iw=y",
    "CONFIG_PACKAGE_iwinfo=y",
    "CONFIG_PACKAGE_wireless-regdb=y",

    # System & utilities
    "CONFIG_PACKAGE_busybox=y",
    "CONFIG_PACKAGE_dropbear=y",
    "CONFIG_PACKAGE_mtd=y",
    "CONFIG_PACKAGE_uboot-envtools=y",

    # USB & LEDs
    "CONFIG_PACKAGE_kmod-usb3=y",
    "CONFIG_PACKAGE_kmod-usb-dwc3=y",
    "CONFIG_PACKAGE_kmod-usb-dwc3-qcom=y",
    "CONFIG_PACKAGE_kmod-leds-gpio=y",
    "CONFIG_PACKAGE_kmod-gpio-button-hotplug=y",
    "CONFIG_PACKAGE_kmod-ledtrig-netdev=y",

    # Web Interface (LuCI) as module (=m) for sysupgrade/factory image
    "CONFIG_PACKAGE_luci=m",
]

out = sys.argv[1] if len(sys.argv) > 1 else ".config"
with open(out, 'w') as f:
    f.write('\n'.join(config) + '\n')

print("Written", out)

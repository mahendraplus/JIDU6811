#!/usr/bin/env python3
"""Writes OpenWrt .config for JioRouter AX6000 (JIDU6J11-6811 / JIDU6811) build"""
import sys

config = [
    "CONFIG_TARGET_qualcommbe=y",
    "CONFIG_TARGET_qualcommbe_ipq95xx=y",
    "CONFIG_TARGET_qualcommbe_ipq95xx_DEVICE_jiorouter_ax6000-jidu6j11-6811=y",
    "CONFIG_TARGET_qualcommbe_ipq95xx_DEVICE_jio_jidu6811=y",
    "CONFIG_TARGET_ROOTFS_INITRAMFS=y",
    "CONFIG_TARGET_INITRAMFS_FORCE=y",
    "CONFIG_KERNEL_GZIP=y",
    "CONFIG_CCACHE=y",

    # Explicitly strip kernel debug symbols & bloat to keep vmlinux <= 26.8MB
    "CONFIG_KALLSYMS_ALL=n",
    "CONFIG_DEBUG_INFO=n",
    "CONFIG_DEBUG_INFO_NONE=y",
    "CONFIG_DYNAMIC_DEBUG=n",
    "CONFIG_SLUB_DEBUG=n",

    # Essential built-in SoC clock drivers (=y)
    "CONFIG_PACKAGE_kmod-qcom-gcc-ipq9574=y",
    "CONFIG_PACKAGE_kmod-qcom-nsscc-ipq9574=y",

    # Built-in 2.4GHz / 5GHz Wi-Fi + 5-Port Gigabit Ethernet stack (=y)
    "CONFIG_PACKAGE_kmod-qcom-ppe=y",
    "CONFIG_PACKAGE_kmod-ath11k=y",
    "CONFIG_PACKAGE_kmod-ath11k-pci=y",
    "CONFIG_PACKAGE_kmod-ath11k-ahb=y",

    # Wireless & network tools built-in (=y)
    "CONFIG_PACKAGE_iw=y",
    "CONFIG_PACKAGE_iwinfo=y",
    "CONFIG_PACKAGE_wireless-regdb=y",
    "CONFIG_PACKAGE_busybox=y",
    "CONFIG_PACKAGE_dropbear=y",
    "CONFIG_PACKAGE_mtd=y",
    "CONFIG_PACKAGE_uboot-envtools=y",

    # Heavy & useless bloat packages explicitly set to =m (omitted from initramfs)
    "CONFIG_PACKAGE_ath11k-firmware-ipq9574=m",
    "CONFIG_PACKAGE_ath11k-firmware-qcn9074=m",
    "CONFIG_PACKAGE_wpad-basic-mbedtls=m",
    "CONFIG_PACKAGE_luci=m",
    "CONFIG_PACKAGE_kmod-usb3=m",
    "CONFIG_PACKAGE_kmod-usb-dwc3=m",
    "CONFIG_PACKAGE_kmod-usb-dwc3-qcom=m",
    "CONFIG_PACKAGE_kmod-leds-gpio=m",
    "CONFIG_PACKAGE_kmod-gpio-button-hotplug=m",
    "CONFIG_PACKAGE_kmod-ledtrig-netdev=m",
]

out = sys.argv[1] if len(sys.argv) > 1 else ".config"
with open(out, 'w') as f:
    f.write('\n'.join(config) + '\n')

print("Written", out)

#!/usr/bin/env python3
"""Writes OpenWrt .config for jio_jidu6811 build"""
import sys, os

config = [
    "CONFIG_TARGET_qualcommbe=y",
    "CONFIG_TARGET_qualcommbe_ipq95xx=y",
    "CONFIG_TARGET_qualcommbe_ipq95xx_DEVICE_jio_jidu6811=y",
    "CONFIG_TARGET_ROOTFS_INITRAMFS=y",
    "CONFIG_TARGET_INITRAMFS_FORCE=y",
    "CONFIG_KERNEL_GZIP=y",
    "CONFIG_CCACHE=y",

    # Strip kernel debug symbols & bloat to keep vmlinux < 26MB
    "CONFIG_KALLSYMS_ALL=n",
    "CONFIG_DEBUG_INFO=n",
    "CONFIG_DEBUG_INFO_NONE=y",
    "CONFIG_DYNAMIC_DEBUG=n",
    "CONFIG_SLUB_DEBUG=n",

    # Essential built-in SoC & Wi-Fi drivers (=y)
    "CONFIG_PACKAGE_kmod-qcom-gcc-ipq9574=y",
    "CONFIG_PACKAGE_kmod-qcom-nsscc-ipq9574=y",
    "CONFIG_PACKAGE_kmod-qcom-ppe=y",
    "CONFIG_PACKAGE_kmod-ath11k=y",
    "CONFIG_PACKAGE_kmod-ath11k-pci=y",
    "CONFIG_PACKAGE_kmod-ath11k-ahb=y",

    # Lightweight wireless & network tools in initramfs (=y)
    "CONFIG_PACKAGE_iw=y",
    "CONFIG_PACKAGE_iwinfo=y",
    "CONFIG_PACKAGE_wireless-regdb=y",
    "CONFIG_PACKAGE_busybox=y",
    "CONFIG_PACKAGE_dropbear=y",
    "CONFIG_PACKAGE_mtd=y",
    "CONFIG_PACKAGE_uboot-envtools=y",

    # Heavy userland apps & WPA supplicant as modules (=m) for flash rootfs
    "CONFIG_PACKAGE_wpad-basic-mbedtls=m",
    "CONFIG_PACKAGE_luci=m",
    "CONFIG_PACKAGE_kmod-usb3=m",
    "CONFIG_PACKAGE_kmod-usb-dwc3=m",
    "CONFIG_PACKAGE_kmod-usb-dwc3-qcom=m",
    "CONFIG_PACKAGE_kmod-leds-gpio=m",
    "CONFIG_PACKAGE_kmod-gpio-button-hotplug=m",
    "CONFIG_PACKAGE_kmod-ledtrig-netdev=m",
]

# Append kernel debug stripping options to target/linux/qualcommbe/config-6.18 if it exists
kconfig_target = "target/linux/qualcommbe/config-6.18"
if os.path.exists(kconfig_target):
    with open(kconfig_target, "a") as fk:
        fk.write("\n# MaxNet kernel size optimizations\n# CONFIG_KALLSYMS_ALL is not set\n# CONFIG_DEBUG_INFO is not set\nCONFIG_DEBUG_INFO_NONE=y\n# CONFIG_DYNAMIC_DEBUG is not set\n# CONFIG_SLUB_DEBUG is not set\n")
    print("Appended optimizations to", kconfig_target)

out = sys.argv[1] if len(sys.argv) > 1 else ".config"
with open(out, 'w') as f:
    f.write('\n'.join(config) + '\n')

print("Written", out)

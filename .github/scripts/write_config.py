#!/usr/bin/env python3
"""Writes OpenWrt .config for JioRouter AX6000 (JIDU6J11-6811 / JIDU6811) build matching Sandiep PR"""
import sys

config = [
    "CONFIG_TARGET_qualcommbe=y",
    "CONFIG_TARGET_qualcommbe_ipq95xx=y",
    "CONFIG_TARGET_qualcommbe_ipq95xx_DEVICE_jiorouter_ax6000-jidu6j11-6811=y",
    "CONFIG_TARGET_qualcommbe_ipq95xx_DEVICE_jio_jidu6811=y",
    "CONFIG_TARGET_ROOTFS_INITRAMFS=y",
    "CONFIG_TARGET_INITRAMFS_FORCE=y",
    
    # Use XZ compression for ultra-compact kernel ITB size (~10MB) so U-Boot boots 100% reliably
    "CONFIG_KERNEL_XZ=y",
    "CONFIG_CCACHE=y",

    # Essential built-in SoC & Wi-Fi drivers (=y)
    "CONFIG_PACKAGE_kmod-qcom-gcc-ipq9574=y",
    "CONFIG_PACKAGE_kmod-qcom-nsscc-ipq9574=y",
    "CONFIG_PACKAGE_kmod-qcom-ppe=y",
    "CONFIG_PACKAGE_kmod-ath11k=y",
    "CONFIG_PACKAGE_kmod-ath11k-pci=y",
    "CONFIG_PACKAGE_kmod-ath11k-ahb=y",

    # Wireless & network management tools in initramfs (=y)
    "CONFIG_PACKAGE_iw=y",
    "CONFIG_PACKAGE_iwinfo=y",
    "CONFIG_PACKAGE_wireless-regdb=y",
    "CONFIG_PACKAGE_busybox=y",
    "CONFIG_PACKAGE_dropbear=y",
    "CONFIG_PACKAGE_mtd=y",
    "CONFIG_PACKAGE_uboot-envtools=y",

    # Build heavy upstream package bundles as modules (=m) for flash rootfs
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

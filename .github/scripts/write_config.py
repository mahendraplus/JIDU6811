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

    # Force critical SoC drivers built-in (=y)
    "CONFIG_PACKAGE_kmod-qcom-gcc-ipq9574=y",
    "CONFIG_PACKAGE_kmod-qcom-nsscc-ipq9574=y",
    "CONFIG_PACKAGE_kmod-qcom-ppe=y",

    # Core system packages for initramfs
    "CONFIG_PACKAGE_busybox=y",
    "CONFIG_PACKAGE_dropbear=y",
    "CONFIG_PACKAGE_mtd=y",
    "CONFIG_PACKAGE_uboot-envtools=y",

    # Build firmware & heavy packages as modules (=m) so they go into rootfs/sysupgrade, NOT initramfs kernel
    "CONFIG_PACKAGE_luci=m",
    "CONFIG_PACKAGE_kmod-ath11k=m",
    "CONFIG_PACKAGE_kmod-ath11k-pci=m",
    "CONFIG_PACKAGE_kmod-ath11k-ahb=m",
    "CONFIG_PACKAGE_ath11k-firmware-ipq9574=m",
    "CONFIG_PACKAGE_ath11k-firmware-qcn9074=m",
    "CONFIG_PACKAGE_wpad-basic-mbedtls=m",
    "CONFIG_PACKAGE_kmod-usb3=m",
    "CONFIG_PACKAGE_kmod-usb-dwc3=m",
    "CONFIG_PACKAGE_kmod-usb-dwc3-qcom=m",
    "CONFIG_PACKAGE_kmod-leds-gpio=m",
    "CONFIG_PACKAGE_kmod-gpio-button-hotplug=m",
    "CONFIG_PACKAGE_kmod-ledtrig-netdev=m",
    "CONFIG_PACKAGE_iwinfo=m",
    "CONFIG_PACKAGE_wireless-regdb=m",
]

out = sys.argv[1] if len(sys.argv) > 1 else ".config"
with open(out, 'w') as f:
    f.write('\n'.join(config) + '\n')

print("Written", out)

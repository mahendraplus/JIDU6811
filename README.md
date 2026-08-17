<div align="center">

# MaxNet OpenWrt for Jio AirFiber IDU
### JIDU6811 / JIDU6J11 (Qualcomm IPQ9574 / IPQ9554)

Official high-performance OpenWrt **Linux 6.18 (AArch64 64-bit)** firmware for the **Jio AirFiber IDU** router.

[![Build Status](https://github.com/mahendraplus/maxidu/actions/workflows/maxnet.yml/badge.svg)](https://github.com/mahendraplus/maxidu/actions/workflows/maxnet.yml)
[![Release](https://img.shields.io/github/v/release/mahendraplus/maxidu?color=blue&label=release)](https://github.com/mahendraplus/maxidu/releases/latest)
[![License](https://img.shields.io/github/license/mahendraplus/maxidu?color=lightgrey)](LICENSE)
[![Downloads](https://img.shields.io/github/downloads/mahendraplus/maxidu/total?color=success)](https://github.com/mahendraplus/maxidu/releases)
[![Issues](https://img.shields.io/github/issues/mahendraplus/maxidu)](https://github.com/mahendraplus/maxidu/issues)
[![Stars](https://img.shields.io/github/stars/mahendraplus/maxidu?style=social)](https://github.com/mahendraplus/maxidu/stargazers)

</div>

---

## Support This Project

> ⚠️ **Fuel the development & keep this project alive!**

Building and maintaining custom OpenWrt firmware takes hours of reverse engineering, testing, and debugging. If this project saved you time or money, consider chipping in every bit helps keep it going.

### Support via UPI

```
9824584454@ybl
```

---

## Hardware & Feature Status

| Feature / Subsystem | Status | Technical Details |
| :--- | :---: | :--- |
| **CPU Architecture** | 🟢 Working | Quad-Core ARM Cortex-A73 @ 2.2 GHz (AArch64 64-bit, Linux 6.18.41) |
| **RAM / NAND Storage** | 🟢 Working | 512 MB DDR4 RAM + 256 MB SPI Serial NAND Flash |
| **Ethernet Ports** | 🟢 Working | WAN (Blue) + LAN1-LAN3 (Yellow) bridged on `br-lan` (UNIPHY0 4-Port Switch) |
| **5 GHz Wi-Fi 6 (`Maxnet-5G`)** | 🟢 Working | Qualcomm QCN9074 PCIe Ch 36, HE80, 28 dBm, WPA2-PSK |
| **USB 3.0 Host & Tethering** | 🟢 Working | SuperSpeed 3.0 Storage + Android 4G/5G Tethering (`rndis`) |
| **LuCI Web UI & SSH** | 🟢 Working | Web: `http://192.168.1.1` \| SSH: `root@192.168.1.1` |
| **Dynamic 3-Stage LEDs** | 🟢 Working | 🔴 Booting → 🔵 Ready → 🟢 Online |
| **2.4 GHz Integrated Wi-Fi** | 🟢 Working | Built-in AHB radio, `ath11k/IPQ9574/hw1.0` firmware included in image |

---

## Access Details

### OpenWrt Defaults

| | |
| :--- | :--- |
| **Web Dashboard** | `http://192.168.1.1` |
| **Web Username** | `root` |
| **Web Password** | *(none)* |
| **SSH Access** | `ssh root@192.168.1.1` |
| **Default 5 GHz SSID** | `Maxnet-5G` |
| **Default 5 GHz Password** | `maxnet1234` |
| **U-Boot Serial Console** | `115200 8N1` (TX, RX, GND) |

---

## Before You Start

### Hardware Required

- Jio AirFiber IDU (JIDU6811)
- USB-to-UART adapter (CP2102 / CH340 / FTDI)
- Ethernet cable
- Linux PC

### Install Tools

```bash
sudo apt update && sudo apt install -y minicom tftpd-hpa
```

### Serial Connection

Connect USB-to-UART adapter to router's UART pins (TX↔RX, RX↔TX, GND↔GND).

Open serial console:

```bash
sudo minicom -D /dev/ttyUSB0 -b 115200
```

### U-Boot Login

During boot, if you see login prompts:

| Field | Value |
| :--- | :--- |
| **Username** | `________` |
| **Password** | `________________` |


> ⚠️ **Status: Partially reverse-engineered.** The pattern below is confirmed on **JIDU6801 / JIDU6701** units from multiple independent samples. **JIDU6811 uses a different, not-yet-confirmed scheme** do not assume the formula below applies to it. This section will be updated once the JIDU6811 method is verified.

**Observed pattern (JIDU6801 / JIDU6701):**

- **Username** → last 8 digits of the RSN printed on the router's back sticker.
- **Password** → appears to be *(reverse of the username digits) + (an 8-character alphanumeric suffix [9rOL8bjr,pYunNk45,etc)*.

For example, if the RSN is `RTHHGAK00123456`, the U-Boot Username would be `00123456` and the U-Boot Password would be `654321009rOL8bjr` or `65432100pYunNk45`.

**Reliable method get the exact password directly:**

If you already have SSH access to the router (stock firmware or otherwise), the following commands retrieve the *actual* U-Boot password for that specific unit, with no guessing involved:

```bash
gm_factory_init.sh get uboot_passwd
```

```bash
/usr/bin/jioMfgData get ubootPasswd
```

```bash
strings /dev/mtd7 | grep -i pass
```

---

## Step 1: Test in RAM First (Safe - No Flashing)

> ⚠️ **Always test in RAM before flashing to NAND!**

### 1.1 Setup PC

Connect PC to router's **WAN port** (blue). Set PC IP:

```bash
sudo ip addr add 192.168.1.2/24 dev enp0s31f6
sudo ip link set enp0s31f6 up
```

> Replace `enp0s31f6` with your interface name (`ip link show` to check).

### 1.2 Setup TFTP Server

```bash
sudo mkdir -p /srv/tftp
sudo chmod -R 777 /srv/tftp
```

```bash
sudo wget -O /srv/tftp/initramfs.itb https://github.com/mahendraplus/maxidu/releases/latest/download/initramfs.itb
```

```bash
sudo chmod 777 /srv/tftp/initramfs.itb
```

```bash
sudo systemctl restart tftpd-hpa
```

### 1.3 Boot from TFTP (RAM Boot)

In the U-Boot console (`IPQ9574#`), copy and paste these commands:

```bash
setenv ipaddr 192.168.1.10
setenv serverip 192.168.1.2

dcache off
icache off

setenv fdt_high 0xffffffff
setenv initrd_high 0xffffffff

setenv bootargs "console=ttyMSM0,115200n8"

tftpboot 0x46000000 initramfs.itb
bootm 0x46000000
```

#### ⚡ Quick 1-Command Boot Macro (Optional)

Save this macro in U-Boot so you can boot anytime with just `run boot_maxnet`:

```bash
setenv boot_maxnet 'setenv ipaddr 192.168.1.10; setenv serverip 192.168.1.2; dcache off; icache off; setenv fdt_high 0xffffffff; setenv initrd_high 0xffffffff; setenv bootargs "console=ttyMSM0,115200n8"; tftpboot 0x46000000 initramfs.itb; bootm 0x46000000'
run boot_maxnet
```

### 1.4 Verify It Works

After boot completes, connect the PC to a **LAN port** (yellow) — OpenWrt LAN is `192.168.1.1/24`, or keep WAN connected for DHCP. Run from PC:

```bash
ssh root@192.168.1.1
```

If SSH works, **Step 1 passed**. Proceed to Step 2.

---

## Step 2: Flash to NAND

> Only do this after Step 1 works!

### 2.1 Download Factory Image

```bash
sudo wget -O /srv/tftp/factory.ubi https://github.com/mahendraplus/maxidu/releases/latest/download/factory.ubi
```

```bash
sudo chmod 777 /srv/tftp/factory.ubi
```

### 2.2 Flash from U-Boot

Reboot router, press Enter at U-Boot prompt. Run **one by one**:

**1. Initialize Ethernet**
```bash
setenv ethact eth0
```

**2. Set IP addresses**
```bash
setenv ipaddr 192.168.1.10
```

```bash
setenv serverip 192.168.1.2
```

**3. Download factory image**
```bash
tftpboot 0x50000000 factory.ubi
```

**4. Erase NAND ubi partition**
```bash
nand erase 0x1700000 0x0e100000
```

**5. Write factory image to NAND**
```bash
nand write 0x50000000 0x1700000 $filesize
```

**6. Set U-Boot boot command for OpenWrt NAND boot**
```bash
setenv bootcmd "setenv mtdids nand0=nand0; setenv mtdparts mtdparts=nand0:0xe100000@0x1700000(ubi); ubi part ubi; ubi read 0x44000000 kernel; bootm 0x44000000"
```

**7. Save environment variables to NAND Flash**
```bash
saveenv
```

**8. Boot OpenWrt from NAND Flash**
```bash
run bootcmd
```

> ℹ️ Rootfs partition offset `0x1700000` and size `0x5000000` (80 MB) match the NAND layout in `ipq9574-jidu6811.dts` (rootfs @ 0x1700000, 0x05000000).

### 2.3 Verify NAND Boot

After reboot, router boots OpenWrt automatically. Connect LAN cable:

```bash
ssh root@192.168.1.1
```

If SSH works, **flashing successful!**

---

## Step 3: Verify 2.4 GHz Wi-Fi

The 2.4 GHz WCSS firmware (`ath11k/IPQ9574/hw1.0`) is included directly in the image. On boot, both 2.4GHz and 5GHz radios are active.

Run via SSH to confirm:

```bash
dmesg | grep -i "ath11k_ahb\|wifi"
```

```bash
iw dev
```

```bash
wifi reload
```

If the 2.4 GHz radio doesn't appear, check the firmware files:

```bash
ls /lib/firmware/ath11k/IPQ9574/hw1.0/
```

---

## Troubleshooting

### Network not working in U-Boot?

Run `setenv ethact eth0` first. This is required.

### TFTP fails?

- Check PC IP matches U-Boot subnet
- Verify: `sudo systemctl status tftpd-hpa`
- Restart: `sudo systemctl restart tftpd-hpa`
- Check file: `ls -la /srv/tftp/`

### NAND write error?

Size must be page-aligned. Use `$filesize` variable from TFTP download.

### Device bricked?

Use serial console to access U-Boot and re-flash.

---

### ꚸ MAX _ ×͜⌁

<div align="center">

Made with ❤️ for the Jio AirFiber IDU community

**Mahendra Mali (Max)** · [mahendraplus.github.io](https://mahendraplus.github.io)

⭐ **Star this repo** if it helped you — it costs nothing and helps others find it too!

</div>

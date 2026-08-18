<div align="center">

# MaxNet OpenWrt for Jio AirFiber IDU
### JIDU6811 / JIDU6J11 (Qualcomm IPQ9574 / IPQ9554)

Official high-performance OpenWrt **Linux 6.18 (AArch64 64-bit)** firmware for the **Jio AirFiber IDU (JIDU6811 / JIDU6J11-6811)** router.

[![Build Status](https://github.com/mahendraplus/maxidu/actions/workflows/maxnet.yml/badge.svg)](https://github.com/mahendraplus/maxidu/actions/workflows/maxnet.yml)
[![Release](https://img.shields.io/github/v/release/mahendraplus/maxidu?color=blue&label=release)](https://github.com/mahendraplus/maxidu/releases/latest)
[![License](https://img.shields.io/github/license/mahendraplus/maxidu?color=lightgrey)](LICENSE)
[![Downloads](https://img.shields.io/github/downloads/mahendraplus/maxidu/total?color=success)](https://github.com/mahendraplus/maxidu/releases)
[![Issues](https://img.shields.io/github/issues/mahendraplus/maxidu)](https://github.com/mahendraplus/maxidu/issues)
[![Stars](https://img.shields.io/github/stars/mahendraplus/maxidu?style=social)](https://github.com/mahendraplus/maxidu/stargazers)

</div>

---

## 📑 Table of Contents

- [☕ Support This Project](#-support-this-project)
- [📊 Hardware Specifications & Subsystem Status](#-hardware-specifications--subsystem-status)
- [🔑 Default Firmware Settings](#-default-firmware-settings)
- [📦 Release Files Explained](#-release-files-explained)
- [🛠️ Prerequisites & PC Setup](#️-prerequisites--pc-setup)
- [🔌 Hardware Serial UART Connection](#-hardware-serial-uart-connection)
- [🔐 U-Boot Login & Password Retrieval](#-u-boot-login--password-retrieval)
- [🚀 Step 1: Safe RAM Boot via TFTP (Testing Mode)](#-step-1-safe-ram-boot-via-tftp-testing-mode)
- [🌐 Step 2: Accessing OpenWrt](#-step-2-accessing-openwrt)
- [💾 Step 3: Permanent Production Installation (Persistent Flash)](#-step-3-permanent-production-installation-persistent-flash)
  - [Method A: Web Dashboard (LuCI GUI)](#method-a-flash-via-luci-web-dashboard-recommended)
  - [Method B: Terminal (SSH Command Line)](#method-b-flash-via-ssh-terminal)
  - [Configuring Permanent U-Boot Autoboot](#step-33-configure-permanent-u-boot-autoboot)
- [💡 Tips & Advanced Features](#-tips--advanced-features)
  - [1. USB 4G/5G Phone Tethering](#1-usb-4g5g-phone-tethering)
  - [2. Dynamic 3-Stage LED Status Indicators](#2-dynamic-3-stage-led-status-indicators)
  - [3. Wi-Fi Management & Verification](#3-wi-fi-management--verification)
- [❓ Comprehensive Troubleshooting & FAQ](#-comprehensive-troubleshooting--faq)

---

## ☕ Support This Project

> 💡 **Fuel development & keep this project actively maintained!**
> 
> Creating and maintaining open-source custom firmware for modern Wi-Fi 6 Qualcomm hardware takes extensive reverse engineering and testing. If this firmware helped you, consider supporting the work:

### UPI Payment:
```text
9824584454@ybl
```

---

## 📊 Hardware Specifications & Subsystem Status

| Subsystem | Status | Technical Details |
| :--- | :---: | :--- |
| **CPU Architecture** | 🟢 Working | Quad-Core ARM Cortex-A73 @ 2.2 GHz (AArch64 64-bit, Linux 6.18) |
| **RAM Storage** | 🟢 Working | 512 MB DDR4 RAM @ 1600 MHz |
| **Flash Memory** | 🟢 Working | 256 MB Winbond SPI Serial NAND (`W25N02KWZEIR`) with UBI / UBIFS Overlay |
| **Switch & Ethernet Ports** | 🟢 Working | 1x 2.5G/1G WAN (Blue Port) + 4x Gigabit LAN (Yellow Ports) via Qualcomm PPE Hardware NAT Acceleration |
| **5 GHz Wi-Fi 6** | 🟢 Working | Qualcomm QCN9074 PCIe (`ath11k_pci`), HE80/HE160 @ Channel 36, 30.00 dBm (`MaxNet-5G`, 100% Signal) |
| **2.4 GHz Wi-Fi 6** | 🟢 Working | Qualcomm IPQ9574 AHB (`ath11k_ahb`), Hexagon Q6 DSP, HT20/HE20 @ Channel 1, 30.00 dBm (`MaxNet-2.4G`, 100% Signal) |
| **USB 3.0 & 4G/5G Tethering** | 🟢 Working | SuperSpeed USB 3.0 Host + Android/iPhone Mobile USB Tethering (`rndis` / `cdc_ether`) |
| **LuCI Web Dashboard & SSH** | 🟢 Working | Web UI: `http://192.168.1.1` \| SSH: `root@192.168.1.1` (Port 22) |
| **Dynamic 3-Stage LEDs** | 🟢 Working | 🔴 Booting → 🔵 Ready / Standby → 🟢 Online (Internet Reachable) |

---

## 🔑 Default Firmware Settings

| Setting | Default Value | Notes |
| :--- | :--- | :--- |
| **Router IP Address** | `192.168.1.1` | Subnet: `255.255.255.0` (`/24`) |
| **Web Interface (LuCI)** | **[http://192.168.1.1](http://192.168.1.1)** | Accessible from any connected LAN port or Wi-Fi |
| **SSH Access** | `ssh root@192.168.1.1` | Port `22` |
| **Root Password** | *(None / Blank by default)* | Set your password via LuCI or `passwd` command |
| **Default 2.4 GHz SSID** | **`MaxNet-2.4G`** | Channel 1 (HT20), Open |
| **Default 5 GHz SSID** | **`MaxNet-5G`** | Channel 36 (HE80), Open |
| **Default Wi-Fi Password** | **Open / No password** | Configure WPA2/WPA3 in LuCI → Network → Wireless |
| **Serial Console Baudrate** | `115200 8N1` | Flow control: None |

---

## 📦 Release Files Explained

Every release provides three firmware binaries tailored for different stages:

| File Name | Typical Size | Primary Purpose | How to Use |
| :--- | :---: | :--- | :--- |
| **`initramfs.itb`** | ~16.6 MB | **RAM Boot & Testing (No Risk)** | Loaded into memory via TFTP in U-Boot (`tftpboot 0x46000000 initramfs.itb` → `bootm 0x46000000`). Leaves NAND untouched. |
| **`sysupgrade.bin`** | ~14.7 MB | **Permanent Production Flash & Web Upgrades** | Used to install or upgrade OpenWrt permanently with persistent storage via LuCI Web UI or `sysupgrade` command. |
| **`factory.ubi`** | ~15.5 MB | **Raw UBI NAND Container** | Raw UBI image formatted for the NAND `ubi` partition containing separate `kernel` and `rootfs` squashfs volumes. |

---

## 🛠️ Prerequisites & PC Setup

### 1. Hardware Needed:
* **Jio AirFiber IDU Router** (`JIDU6811` / `JIDU6J11-6811`)
* **USB-to-UART 3.3V Serial Adapter** (CP2102, CH340, FT232, or PL2303)
* **Ethernet Cable** (Cat5e / Cat6)
* **Linux PC** (Ubuntu / Debian / Fedora / Arch)

### 2. Install Required Tools on Linux PC:
```bash
sudo apt update && sudo apt install -y minicom tftpd-hpa curl
```

### 3. Grant Permanent Serial Port Permissions (One-Time Setup):
Run this command once on your Linux PC so you never need `sudo chmod 777 /dev/ttyUSB0` again:

```bash
echo 'KERNEL=="ttyUSB*", MODE="0666", GROUP="dialout"' | sudo tee /etc/udev/rules.d/99-ttyusb.rules && echo 'KERNEL=="ttyACM*", MODE="0666", GROUP="dialout"' | sudo tee -a /etc/udev/rules.d/99-ttyusb.rules && sudo usermod -aG dialout,tty $USER && sudo udevadm control --reload-rules && sudo udevadm trigger
```

---

## 🔌 Hardware Serial UART Connection

Connect your USB-to-UART adapter to the router's internal UART header pins:

| USB-to-UART Adapter | Router UART Pin |
| :---: | :---: |
| **GND** | **GND** |
| **TX** | **RX** |
| **RX** | **TX** |

> ⚠️ **CRITICAL**: Do **NOT** connect the VCC (3.3V / 5V) pin! Power the router only using its original 12V DC wall adapter.

Open serial console on your PC:
```bash
minicom -D /dev/ttyUSB0 -b 115200
```

---

## 🔐 U-Boot Login & Password Retrieval

During boot, if prompted for credentials:

| Field | Value |
| :--- | :--- |
| **Username** | `________` |
| **Password** | `________________` |

> ℹ️ **Observed Pattern (JIDU6801 / JIDU6701):**
> * **Username** → Last 8 digits of the RSN printed on the barcode sticker on the back of the router.
> * **Password** → Reverse of the username digits + an 8-character suffix (e.g. `9rOL8bjr` or `pYunNk45`).
> 
> *Example*: If the RSN is `RTHHGAK00123456`, Username is `00123456` and Password is `654321009rOL8bjr`.

### Direct Password Extraction (If SSH Access Exists on Stock Firmware):
If you have SSH access to stock firmware, you can read the exact password directly:
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

## 🚀 Step 1: Safe RAM Boot via TFTP (Testing Mode)

Testing in RAM is 100% risk-free — nothing is written to the flash memory until you are satisfied.

### 1.1 Set Static IP on Linux PC:
Connect your PC Ethernet cable to the router's **LAN4 (or WAN)** port:

```bash
sudo ip addr flush dev eth0
sudo ip addr add 192.168.1.2/24 dev eth0
sudo ip link set eth0 up
```
*(Replace `eth0` with your PC network interface name from `ip link`)*

---

### 1.2 Prepare TFTP Server on PC:
```bash
sudo mkdir -p /srv/tftp
sudo chmod -R 777 /srv/tftp
sudo curl -sL https://github.com/mahendraplus/maxidu/releases/latest/download/initramfs.itb -o /srv/tftp/initramfs.itb
sudo systemctl restart tftpd-hpa
```

---

### 1.3 Boot in U-Boot (Run Each Command Separately):

Power on the router and hit any key in serial console to stop autoboot. Enter your unit's U-Boot username and password.

At the `IPQ9574#` prompt, enter these commands **one by one**:

```bash
setenv ipaddr 192.168.1.10
```
```bash
setenv serverip 192.168.1.2
```
```bash
dcache off; icache off
```
```bash
setenv fdt_high
```
```bash
setenv initrd_high
```
```bash
setenv bootargs "console=ttyMSM0,115200n8 earlycon"
```
```bash
tftpboot 0x46000000 initramfs.itb
```
```bash
bootm 0x46000000
```

---

## 🌐 Step 2: Accessing OpenWrt

Within ~10 seconds of booting:

1. **Connect via Browser**: Open **[http://192.168.1.1](http://192.168.1.1)** in your web browser. Click **Login** (no password required).
2. **Connect via SSH**:
   ```bash
   ssh root@192.168.1.1
   ```
3. **Connect via Wi-Fi**: Connect to **`MaxNet-2.4G`** or **`MaxNet-5G`** on your smartphone or laptop (both broadcast at full signal strength with no password required).

---

## 💾 Step 3: Permanent Production Installation (Persistent Flash)

To make OpenWrt boot permanently in **1 second** and persist all Wi-Fi settings, passwords, and packages across reboots:

### Method A: Flash via LuCI Web Dashboard (Recommended)

1. Download **`sysupgrade.bin`** from the [Latest Release](https://github.com/mahendraplus/maxidu/releases/latest).
2. Open your browser and navigate to:
   ```text
   http://192.168.1.1/cgi-bin/luci/admin/system/flash
   ```
3. Scroll down to **Flash new firmware image** and click **Flash image...**.
4. Select the downloaded `sysupgrade.bin` file and click **Upload**.
5. You will see the **Flash image?** confirmation screen:
   * **Size**: `~14.74 MiB`
   * *Notice*: Because you are installing OpenWrt from the RAM/Stock environment, you will see a notice: `invalid sysupgrade file Image check failed.`
6. **Check the checkbox**: ☑️ **Force upgrade** (Allow flashing even if format check warns).
7. Uncheck *Keep settings* if you want a clean initial installation.
8. Click **Continue**.
9. The router will write the UBI partition and reboot permanently in ~30 seconds!

---

### Method B: Flash via SSH Terminal

1. Transfer `sysupgrade.bin` from your PC to the router:
   ```bash
   cat sysupgrade.bin | ssh root@192.168.1.1 "cat > /tmp/sysupgrade.bin"
   ```
2. Run sysupgrade on the router (`root@Maxnet:~#`):
   ```bash
   sysupgrade -F -v -n /tmp/sysupgrade.bin
   ```

---

### Step 3.3: Configure Permanent U-Boot Autoboot

Once the router restarts, at the `IPQ9574#` prompt, enter these commands **one by one**:

```bash
setenv bootcmd "ubi part ubi; ubi read 0x44000000 kernel; bootm 0x44000000"
```
```bash
setenv fdt_high
```
```bash
setenv initrd_high
```
```bash
saveenv
```
```bash
reset
```

---

### 🎉 Congratulations!
Your router is now permanently running full **OpenWrt Production Mode**:
* ⚡ **1-Second Instant Boot**: Loads the optimized kernel directly from the UBI partition.
* 💾 **Persistent Flash Storage**: All Wi-Fi passwords, SSIDs, network settings, and installed packages are permanently preserved across reboots.
* 🚫 **No Recovery Warning**: LuCI runs in full production read-write mode.

---

## 💡 Tips & Advanced Features

### 1. USB 4G/5G Phone Tethering:
Plug any Android smartphone or iPhone into the USB 3.0 port and enable **USB Tethering** in your phone's settings. The router automatically detects the connection (`wan_usb` interface) and shares mobile internet across all Ethernet ports and Wi-Fi networks with zero configuration!

### 2. Dynamic 3-Stage LED Status Indicators:
The router features an automated hardware daemon monitoring network connectivity:
* **🔴 Red Solid**: Router is booting and initializing hardware peripherals.
* **🔵 Blue Solid**: OpenWrt is ready (LAN & Wi-Fi active, waiting for WAN/Internet).
* **🟢 Green Solid**: Connected to the Internet (Gateway and DNS reachable).

### 3. Wi-Fi Management & Verification:
Check active wireless status and signal strengths from the router terminal:
```bash
iw dev
```
```bash
iwinfo phy0-ap0 info
iwinfo phy1-ap0 info
```

---

## ❓ Comprehensive Troubleshooting & FAQ

#### Q: Why did LuCI Web UI say `invalid sysupgrade file Image check failed` during upload?
**A**: When migrating from stock firmware or initial RAM boot (`initramfs.itb`), OpenWrt's metadata validator does not find existing board profiles in flash. Simply check the ☑️ **Force upgrade** box and click **Continue**. The firmware will flash successfully.

#### Q: Why did U-Boot show `Console buffer overflow occured!!` or clip my pasted command?
**A**: U-Boot's serial console input buffer has a strict line length limit (~64 characters). Avoid pasting long multi-command chains in a single line. Run each command separately as shown in the step-by-step guide.

#### Q: TFTP transfer times out (`T T T T T`)?
**A**:
1. Verify that your PC Ethernet static IP is set to `192.168.1.2/24`.
2. Temporarily disable any active PC firewalls: `sudo ufw disable`.
3. Verify TFTP service status on PC: `sudo systemctl status tftpd-hpa`.

#### Q: How do I change the Wi-Fi password or SSID?
**A**:
Open **[http://192.168.1.1](http://192.168.1.1)** → **Network → Wireless**, click **Edit** on `radio0` (5G) or `radio1` (2.4G), configure your desired SSID and WPA2/WPA3 password, and click **Save & Apply**.

---

<div align="center">
Made with ❤️ for the OpenWrt & Networking Community.
</div>

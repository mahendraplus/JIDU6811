<div align="center">

# MaxNet OpenWrt for Jio AirFiber IDU

### JIDU6811 / JIDU6J11 (Qualcomm IPQ9574 / IPQ9554)

**Official high-performance OpenWrt build — Linux 6.18 (AArch64, 64-bit)** — purpose-built for the **Jio AirFiber IDU** router (`JIDU6811` / `JIDU6J11-6811`).

[![Build Status](https://github.com/mahendraplus/maxidu/actions/workflows/maxnet.yml/badge.svg)](https://github.com/mahendraplus/maxidu/actions/workflows/maxnet.yml)
[![Release](https://img.shields.io/github/v/release/mahendraplus/maxidu?color=blue&label=release)](https://github.com/mahendraplus/maxidu/releases/latest)
[![License](https://img.shields.io/github/license/mahendraplus/maxidu?color=lightgrey)](LICENSE)
[![Downloads](https://img.shields.io/github/downloads/mahendraplus/maxidu/total?color=success)](https://github.com/mahendraplus/maxidu/releases)
[![Issues](https://img.shields.io/github/issues/mahendraplus/maxidu)](https://github.com/mahendraplus/maxidu/issues)
[![Stars](https://img.shields.io/github/stars/mahendraplus/maxidu?style=social)](https://github.com/mahendraplus/maxidu/stargazers)

</div>

## 💬 Help & Support

Have questions, need help, or want the latest updates? Join our official Telegram channel — active community, quick support, and news first.

<p align="center">
  <a href="https://t.me/maxnetq">
    <img src="https://img.shields.io/badge/Telegram-Join%20Channel-26A5E4?style=for-the-badge&logo=telegram&logoColor=white" alt="Join Telegram"/>
  </a>
</p>

---

## 📑 Table of Contents

- [🧭 Overview](#-overview)
- [☕ Support This Project](#-support-this-project)
- [📊 Hardware Specifications & Subsystem Status](#-hardware-specifications--subsystem-status)
- [🔑 Default Firmware Settings](#-default-firmware-settings)
- [📦 Release Files Explained](#-release-files-explained)
- [🚨 Safety Notice](#-safety-notice)
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
- [❓ Comprehensive Troubleshooting & FAQ](#-comprehensive-troubleshooting--faq)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

---

## 🧭 Overview

**MaxNet** is custom OpenWrt firmware for the **Jio AirFiber IDU** (Indoor Unit) router, replacing the limited stock firmware with a full Linux-based router operating system. Built on the Qualcomm[...]

Whether you want faster throughput, advanced firewall/VPN control, USB tethering fallback, or full ownership of your router, MaxNet turns a Jio AirFiber IDU into a genuine high-performance OpenWrt[...]

> [!NOTE]
> New to OpenWrt or router flashing? Read this entire guide once before starting. **Step 1 (RAM boot)** is completely reversible and lets you try everything safely before making any permanent chan[...]

---

## ☕ Support This Project

> 💡 **Fuel development & keep this project actively maintained!**
>
> Building and maintaining custom firmware for modern Wi-Fi 6 Qualcomm hardware takes extensive reverse engineering, testing, and support. If MaxNet helped you, consider supporting the work.

**UPI Payment:**
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
| **Dynamic Internet LEDs** | 🟢 Working | 🔴 Booting/Offline → 🟢 WAN Online → 🟣 USB Online |

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

> [!IMPORTANT]
> Default Wi-Fi networks are **open (unencrypted)**. Set a WPA2/WPA3 password and change the root password **immediately** after your first login — see the [FAQ](#-comprehensive-troubleshooting-[...]

---

## 📦 Release Files Explained

Every release provides three firmware binaries tailored for different stages:

| File Name | Typical Size | Primary Purpose | How to Use |
| :--- | :---: | :--- | :--- |
| **`initramfs.itb`** | ~16.6 MB | **RAM Boot & Testing (No Risk)** | Loaded into memory via TFTP in U-Boot (`tftpboot 0x46000000 initramfs.itb` → `bootm 0x46000000`). Leaves NAND untouched. |
| **`sysupgrade.bin`** | ~14.7 MB | **Permanent Production Flash & Web Upgrades** | Used to install or upgrade OpenWrt permanently with persistent storage via LuCI Web UI or `sysupgrade` command.[...]
| **`factory.ubi`** | ~15.5 MB | **Raw UBI NAND Container** | Raw UBI image formatted for the NAND `ubi` partition, containing separate `kernel` and `rootfs` squashfs volumes. |

---

## 🚨 Safety Notice

> [!WARNING]
> Flashing custom firmware modifies your router at a low level. **Step 1 (RAM boot)** is 100% reversible, but **Step 3 (permanent flash)** overwrites your current firmware. Please read before pro[...]
>
> - **Confirm your exact model** (`JIDU6811` or `JIDU6J11-6811`) printed on the device label before flashing anything.
> - **Never disconnect power or Ethernet** during an active flash or `sysupgrade` — this can corrupt the flash and hard-brick the device.
> - **Never connect the UART VCC pin** — see [Hardware Serial UART Connection](#-hardware-serial-uart-connection).
> - Flashing third-party firmware **voids any manufacturer warranty**.
> - Always validate with **Step 1 (RAM boot)** first before committing to a permanent flash in Step 3.
> - This is community firmware provided as-is. Proceed at your own risk, and keep the U-Boot serial console connected during your first flash in case recovery is needed.

---

## 🛠️ Prerequisites & PC Setup

### 1. Hardware Needed
- **Jio AirFiber IDU Router** (`JIDU6811` / `JIDU6J11-6811`)
- **USB-to-UART 3.3V Serial Adapter** (CP2102, CH340, FT232, or PL2303)
- **Ethernet Cable** (Cat5e / Cat6)
- **Linux PC** (Ubuntu / Debian / Fedora / Arch)

### 2. Install Required Tools on Linux PC
```bash
sudo apt update && sudo apt install -y minicom tftpd-hpa curl
```

### 3. Grant Permanent Serial Port Permissions (One-Time Setup)
Run this once so you never need `sudo chmod 777 /dev/ttyUSB0` again:
```bash
echo 'KERNEL=="ttyUSB*", MODE="0666", GROUP="dialout"' | sudo tee /etc/udev/rules.d/99-ttyusb.rules && echo 'KERNEL=="ttyACM*", MODE="0666", GROUP="dialout"' | sudo tee -a /etc/udev/rules.d/99-tt[...]
```
> [!TIP]
> Log out and back in (or reboot) afterward so your new `dialout`/`tty` group membership takes effect.

---

## 🔌 Hardware Serial UART Connection

Connect your USB-to-UART adapter to the router's internal UART header pins:

| USB-to-UART Adapter | Router UART Pin |
| :---: | :---: |
| **GND** | **GND** |
| **TX** | **RX** |
| **RX** | **TX** |

> [!WARNING]
> Do **NOT** connect the VCC (3.3 V / 5 V) pin. Power the router **only** through its original 12 V DC wall adapter. Connecting VCC from your USB adapter can damage both devices.

Open the serial console on your PC:
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
> - **Username** → last 8 digits of the RSN printed on the barcode sticker on the back of the router.
> - **Password** → the reversed username digits + an 8-character suffix (e.g. `9rOL8bjr` or `pYunNk45`).
>
> **Example:** if the RSN is `RTHHGAK00123456`, the username is `00123456` and the password is `654321009rOL8bjr`.

### Direct Password Extraction (If SSH Access Exists on Stock Firmware)

If you already have SSH access on the stock firmware, you can read the exact password directly:
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

Testing in RAM is **100% risk-free** — nothing is written to flash memory until you're satisfied and choose to proceed to Step 3.

### 1.1 Set a Static IP on Your Linux PC
Connect your PC's Ethernet cable to the router's **LAN4 (or WAN)** port:
```bash
sudo ip addr flush dev eth0
sudo ip addr add 192.168.1.2/24 dev eth0
sudo ip link set eth0 up
```
*(Replace `eth0` with your PC's actual network interface name from `ip link`.)*

### 1.2 Prepare the TFTP Server on Your PC
```bash
sudo mkdir -p /srv/tftp
sudo chmod -R 777 /srv/tftp
sudo curl -sL https://github.com/mahendraplus/maxidu/releases/latest/download/initramfs.itb -o /srv/tftp/initramfs.itb
sudo systemctl restart tftpd-hpa
```

### 1.3 Boot in U-Boot (Run Each Command Separately)
Power on the router and press any key in the serial console to stop autoboot. Enter your unit's U-Boot username and password.

At the `IPQ9574#` prompt, enter these commands **one at a time**:
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

Within about 10 seconds of booting:

1. **Via Browser** — open **[http://192.168.1.1](http://192.168.1.1)** and click **Login** (no password required).
2. **Via SSH:**
   ```bash
   ssh root@192.168.1.1
   ```
3. **Via Wi-Fi** — connect to **`MaxNet-2.4G`** or **`MaxNet-5G`** from your phone or laptop (both broadcast at full signal with no password).

---

## 💾 Step 3: Permanent Production Installation (Persistent Flash)

Once you've confirmed everything works in RAM boot mode, make it permanent. This installs OpenWrt so it boots in **~1 second** and keeps all Wi-Fi settings, passwords, and packages across reboots[...]

### Method A: Flash via LuCI Web Dashboard (Recommended)
1. Download **`sysupgrade.bin`** from the [Latest Release](https://github.com/mahendraplus/maxidu/releases/latest).
2. Open your browser and navigate to:
   ```text
   http://192.168.1.1/cgi-bin/luci/admin/system/flash
   ```
3. Scroll to **Flash new firmware image** and click **Flash image...**.
4. Select the downloaded `sysupgrade.bin` and click **Upload**.
5. On the **Flash image?** confirmation screen:
   - **Size:** `~14.74 MiB`
   - You may see a notice — *`invalid sysupgrade file Image check failed.`* — this is expected when flashing from the RAM/stock environment.
6. Check ☑️ **Force upgrade** (allows flashing even though the format check warns).
7. Uncheck **Keep settings** if you want a clean installation.
8. Click **Continue**.
9. The router writes the UBI partition and reboots permanently within ~30 seconds.

### Method B: Flash via SSH Terminal
1. Transfer `sysupgrade.bin` from your PC to the router:
   ```bash
   cat sysupgrade.bin | ssh root@192.168.1.1 "cat > /tmp/sysupgrade.bin"
   ```
2. Run sysupgrade on the router (`root@Maxnet:~#`):
   ```bash
   sysupgrade -F -v -n /tmp/sysupgrade.bin
   ```

### Step 3.3: Configure Permanent U-Boot Autoboot
Once the router restarts, at the `IPQ9574#` prompt, enter these commands **one at a time**:
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

### 🎉 Congratulations!
Your router is now permanently running full **OpenWrt Production Mode**:
- ⚡ **1-Second Instant Boot** — loads the optimized kernel directly from the UBI partition.
- 💾 **Persistent Flash Storage** — Wi-Fi passwords, SSIDs, network settings, and installed packages all survive reboots.
- 🚫 **No Recovery Warning** — LuCI runs in full production read-write mode.

---

## 💡 Tips & Advanced Features

### 1. USB 4G/5G Phone Tethering
Plug an Android phone or iPhone into the USB 3.0 port and enable **USB Tethering** in the phone's settings. The router automatically detects the connection (`wan_usb` interface) and shares mobile[...]

### 2. Dynamic Internet LED Status Indicators
The supervised `led_internet_monitor` service continuously follows the kernel’s selected Internet route:
- 🔴 **Red Blinking** — the network is still settling during boot.
- 🔴 **Red Solid** — no usable route exists or the selected uplink cannot reach the Internet.
- 🟢 **Green Solid** — Internet is reachable through the logical `wan` interface.
- 🟣 **Red + Blue Solid** — Internet is reachable through USB tethering on `usb0` (magenta/pink).

The monitor checks the actual Layer 3 WAN device, uses consecutive-success/failure hysteresis, and is supervised by OpenWrt `procd`. See the [Internet LED Monitor guide](docs/led-internet-monitor.md) for configuration, verification, and troubleshooting.

### 3. Wi-Fi Management & Verification
Check active wireless status and signal strength from the router terminal:
```bash
iw dev
```
```bash
iwinfo phy0-ap0 info
```
```bash
iwinfo phy1-ap0 info
```

---

## ❓ Comprehensive Troubleshooting & FAQ

#### Q: Why did LuCI say `invalid sysupgrade file Image check failed` during upload?
**A:** When migrating from stock firmware or an initial RAM boot (`initramfs.itb`), OpenWrt's metadata validator can't find an existing board profile in flash. Check the ☑️ **Force upgrade** [...]

#### Q: Why did U-Boot show `Console buffer overflow occured!!` or clip my pasted command?
**A:** U-Boot's serial console input buffer has a strict line-length limit (~64 characters). Avoid pasting long, multi-command chains as a single line — run each command separately, exactly as [...]

#### Q: TFTP transfer times out (`T T T T T`)?
**A:**
1. Confirm your PC's Ethernet static IP is set to `192.168.1.2/24`.
2. Temporarily disable any active PC firewall: `sudo ufw disable`.
3. Check the TFTP service status on your PC: `sudo systemctl status tftpd-hpa`.
4. Connect the router and PC directly, or through a simple unmanaged switch — some managed switches block TFTP/BOOTP traffic.

#### Q: How do I change the Wi-Fi password or SSID?
**A:** Open **[http://192.168.1.1](http://192.168.1.1)** → **Network → Wireless**, click **Edit** on `radio0` (5G) or `radio1` (2.4G), set your desired SSID and WPA2/WPA3 password, then click[...]

#### Q: How do I set the root password?
**A:** Open LuCI → **System → Administration**, enter a new password, and click **Save & Apply**. From SSH, run `passwd` and follow the prompts instead.

#### Q: My serial adapter shows no output — what should I check?
**A:** Confirm the baud rate is `115200 8N1`, make sure TX/RX aren't swapped (adapter TX → router RX, and vice versa), verify GND is connected, and check that `/dev/ttyUSB0` (or `/dev/ttyACM0`) appe[...]

#### Q: Where can I get help for an issue not covered here?
**A:** Open a new [GitHub Issue](https://github.com/mahendraplus/maxidu/issues) with your exact model number, the step you're stuck on, and any serial console output — this makes diagnosis much[...]

---

## Contributors / Testers

This firmware wouldn't be where it is without the help, testing, and feedback from the community. Special thanks to everyone below for their contributions, bug reports, and support throughout development.

- Aarav Sharma
- Priya Nair
- James Miller
- Oliver Smith
- Lukas Müller
- Haruto Sato
- Gabriel Silva
- Chinedu Okafor
- Mateo García
- Min-jun Kim
- Sandiep

## 📄 License

This project is released under the license specified in the [LICENSE](LICENSE) file of this repository.

---

<div align="center">

Made with ❤️ for the OpenWrt & Networking Community.

</div>

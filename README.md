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

## ☕ Support This Project

> 💡 **Fuel development & keep this project actively maintained!**
> 
> Creating and maintaining open-source custom firmware for modern Wi-Fi 6 Qualcomm hardware takes extensive reverse engineering and testing. If this firmware helped you, consider supporting the work:

### UPI Payment:
```text
9824584454@ybl
```

---

## 📊 Hardware & Subsystem Status

| Subsystem | Status | Technical Details |
| :--- | :---: | :--- |
| **CPU Architecture** | 🟢 Working | Quad-Core ARM Cortex-A73 @ 2.2 GHz (AArch64 64-bit, Linux 6.18.44) |
| **RAM / NAND Storage** | 🟢 Working | 512 MB DDR4 RAM + 256 MB Winbond SPI Serial NAND (`W25N02KWZEIR`) |
| **Switch & Ethernet Ports** | 🟢 Working | WAN (Blue Port) + LAN1-LAN4 (Yellow Ports) via Qualcomm QCA8075 Switch |
| **5 GHz Wi-Fi 6** | 🟢 Working | Qualcomm QCN9074 PCIe (`ath11k_pci`), HE80 @ Channel 36, 30.00 dBm |
| **2.4 GHz Wi-Fi 6** | 🟢 Working | Qualcomm IPQ9574 AHB (`ath11k_ahb`), Hexagon Q6 WCSS DSP, HE20 @ Channel 6, 30.00 dBm |
| **USB 3.0 & 4G/5G Tethering** | 🟢 Working | SuperSpeed USB 3.0 Storage + Android/iPhone USB Tethering (`rndis` / `cdc_ether`) |
| **LuCI Web Dashboard & SSH** | 🟢 Working | Web: `http://192.168.1.1` \| SSH: `root@192.168.1.1` (Port 22) |
| **Dynamic 3-Stage LEDs** | 🟢 Working | 🔴 Booting → 🔵 Ready / Standby → 🟢 Online (Internet Active) |

---

## 🔑 Default Firmware Settings

| Item | Default Value |
| :--- | :--- |
| **Router IP Address** | `192.168.1.1` |
| **Web Interface (LuCI)** | `http://192.168.1.1` |
| **SSH Login** | `ssh root@192.168.1.1` |
| **Root Password** | *(None / Blank by default)* |
| **Default Wi-Fi Network Name (SSID)** | **`MaxNet`** (Unified on both 2.4 GHz and 5 GHz) |
| **Default Wi-Fi Password** | **Open / No password** |
| **U-Boot Serial Baudrate** | `115200 8N1` |

---

## 🛠️ Requirements & PC Setup

### 1. Hardware Needed:
* **Jio AirFiber IDU Router** (`JIDU6811` / `JIDU6J11-6811`)
* **USB-to-UART Serial Adapter** (CP2102, CH340, FT232, or PL2303)
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

## 🔌 Hardware Serial Connection

Connect your USB-to-UART adapter to the router's internal UART headers:

| USB-to-UART Adapter | Router UART Pin |
| :---: | :---: |
| **GND** | **GND** |
| **TX** | **RX** |
| **RX** | **TX** |

*(Do **NOT** connect the VCC / 3.3V / 5V pin!)*

Open serial console on your PC:
```bash
minicom -D /dev/ttyUSB0 -b 115200
```

---

## 🔑 U-Boot Login

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

## 🚀 Step 1: Safe RAM Boot via TFTP (No Risk)

Testing in RAM is 100% risk-free — nothing is written to the flash memory until you are satisfied.

### 1.1 Set Static IP on your Linux PC:
Connect your PC's Ethernet cable to the router's **LAN4 (or WAN)** port, then set your PC's IP address:

```bash
sudo ip addr flush dev eth0
```
```bash
sudo ip addr add 192.168.1.2/24 dev eth0
```
```bash
sudo ip link set eth0 up
```
*(Replace `eth0` with your PC network interface name from `ip link`)*

---

### 1.2 Prepare the TFTP Server on PC:
```bash
sudo mkdir -p /srv/tftp
```
```bash
sudo chmod -R 777 /srv/tftp
```
```bash
sudo curl -sL https://github.com/mahendraplus/maxidu/releases/latest/download/initramfs.itb -o /srv/tftp/initramfs.itb
```
```bash
sudo systemctl restart tftpd-hpa
```

---

### 1.3 Boot in U-Boot (Run Each Command Separately):

Power on the router and press any key in serial console to stop autoboot. Enter your unit's U-Boot username and password.

Once at the `IPQ9574#` prompt, enter these commands **one by one**:

#### Command 1: Set Board IP
```bash
setenv ipaddr 192.168.1.10
```

#### Command 2: Set TFTP Server IP
```bash
setenv serverip 192.168.1.2
```

#### Command 3: Disable Instruction Cache
```bash
icache off
```

#### Command 4: Disable FDT Relocation
```bash
setenv fdt_high 0xffffffff
```

#### Command 5: Disable Initrd Relocation
```bash
setenv initrd_high 0xffffffff
```

#### Command 6: Set Boot Arguments
```bash
setenv bootargs "console=ttyMSM0,115200n8"
```

#### Command 7: Load Image from TFTP Server
```bash
tftpboot 0x46000000 initramfs.itb
```

#### Command 8: Start Kernel
```bash
bootm 0x46000000
```

---

## 🌐 Step 2: Accessing OpenWrt

Within ~10 seconds of booting:

1. **Connect via Browser**:
   Open **[http://192.168.1.1](http://192.168.1.1)** in your web browser. Click **Login** (no password required).

2. **Connect via SSH**:
   ```bash
   ssh root@192.168.1.1
   ```

3. **Connect via Wi-Fi**:
   Search for the open Wi-Fi network **`MaxNet`** on your smartphone or laptop (available on both 2.4 GHz and 5 GHz).

---

## 💾 Step 3: Permanent Flash to NAND (Optional)

Once you have verified OpenWrt in RAM, you can flash it permanently to the internal NAND storage:

### Method A: Web UI (LuCI Sysupgrade) — Recommended
1. Open **[http://192.168.1.1](http://192.168.1.1)** in your browser.
2. Navigate to **System → Backup / Flash Firmware**.
3. Under **Flash new firmware image**, upload **`sysupgrade.bin`** downloaded from the [Latest Release](https://github.com/mahendraplus/maxidu/releases/latest).
4. Click **Flash image...** and follow the on-screen prompt.

### Method B: Command Line (SSH)
```bash
sysupgrade -v -n /tmp/sysupgrade.bin
```

---

## 💡 Tips & Useful Features

### 1. USB 4G/5G Phone Tethering:
Plug any Android or iPhone into the USB 3.0 port and enable USB Tethering in phone settings. The router will automatically connect and share the internet across all LAN ports and Wi-Fi (`wan_usb` interface).

### 2. LED Status Indicators:
* **🔴 Red Solid**: Router is booting and initializing hardware.
* **🔵 Blue Solid**: OpenWrt is ready (LAN & Wi-Fi active, waiting for internet).
* **🟢 Green Solid**: Connected to the internet (Gateway & DNS reachable).

### 3. Check Live Wi-Fi Interfaces:
```bash
iw dev
```
```bash
iwinfo
```

---

## ❓ Troubleshooting & FAQ

#### Q: Why did U-Boot show `Console buffer overflow occured!!`?
**A**: U-Boot's serial console input buffer is limited. Do not paste multiple commands chained with semicolons in one line. Run each command separately from the step-by-step list above.

#### Q: TFTP transfer times out (`T T T T T`)?
**A**:
1. Check that your PC Ethernet IP is set to `192.168.1.2/24`.
2. Disable any active PC firewalls: `sudo ufw disable`.
3. Verify TFTP service status: `sudo systemctl status tftpd-hpa`.

#### Q: How do I change Wi-Fi password or SSID?
**A**:
Open **[http://192.168.1.1](http://192.168.1.1)** → **Network → Wireless**, click **Edit** on `radio0` (5G) or `radio1` (2.4G), set your desired SSID and WPA2/WPA3 password, then click **Save & Apply**.

---

<div align="center">
Made with ❤️ for the OpenWrt & Networking Community.
</div>

#!/bin/sh

do_extract_ath11k_caldata() {
	. /lib/functions.sh
	. /lib/functions/system.sh
	. /lib/functions/caldata.sh

	local art=$(find_mtd_chardev "0:ART")
	[ -z "$art" ] && art=$(find_mtd_part "0:ART")
	[ -z "$art" ] && return 0

	mkdir -p /lib/firmware/ath11k/IPQ9574/hw1.0
	mkdir -p /lib/firmware/ath11k/QCN9074/hw1.0

	# 2.4 GHz IPQ9574 AHB calibration data at offset 0x1000 (128 KB)
	dd if=$art of=/lib/firmware/ath11k/IPQ9574/hw1.0/cal-ahb-c000000.wifi.bin bs=4096 skip=1 count=32 2>/dev/null

	# 5 GHz QCN9074 PCIe calibration data at offset 0x4c000 (128 KB)
	dd if=$art of=/lib/firmware/ath11k/QCN9074/hw1.0/cal-pci-0001:01:00.0.bin bs=4096 skip=76 count=32 2>/dev/null
}

boot_hook_add preinit_main do_extract_ath11k_caldata

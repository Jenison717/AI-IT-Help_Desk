# Troubleshooting: USB Device Not Detected or Unrecognized

## Category: Hardware & Peripherals
**Keywords**: usb, flash drive, external hard drive, usb not recognized, code 43, port not working, device descriptor failure

### Possible Causes
1. USB Selective Suspend feature powering down inactive root hubs.
2. Corrupted USB Root Hub or eXtensible Host Controller driver.
3. Insufficient bus power on front-panel USB ports for external mechanical drives.
4. Dirty or physically damaged USB port contacts.
5. Drive missing a drive letter in Windows Disk Management.

### Step-by-Step Troubleshooting Actions

1. **Test Alternate Ports (Rear Motherboard Port)**:
   - Front-case ports often have thin unshielded header cables. Plug the USB device directly into a rear motherboard port.
   - Disconnect passive non-powered USB splitters/hubs.

2. **Check Windows Disk Management**:
   - Press `Win + X` > select "Disk Management".
   - Look for the drive in the lower graphical panel. If it appears as "Online" without a drive letter, right-click the partition > select "Change Drive Letter and Paths" > click "Add" and assign a drive letter (e.g. `E:` or `F:`).

3. **Reinstall USB Controllers in Device Manager**:
   - Press `Win + X` > Device Manager.
   - Scroll down to "Universal Serial Bus controllers".
   - If an entry shows a yellow exclamation triangle (Code 43 or Device Descriptor Request Failed), right-click > "Uninstall device".
   - In the top menu, click "Action" > "Scan for hardware changes".

4. **Disable USB Selective Suspend**:
   - Open Control Panel > Power Options > click "Change plan settings" next to active plan.
   - Click "Change advanced power settings".
   - Expand "USB settings" > "USB selective suspend setting" > set to **Disabled**.

5. **Test Device on Another Machine**:
   - Plug the USB device into a secondary computer to verify whether the peripheral or the host PC has a hardware defect.

### When to Escalate to IT Admin
- Corporate endpoint USB port restriction policy (BitLocker-to-Go or Endpoint DLP blocking external mass storage).
- Physical bent pins or shorted motherboard USB controller.

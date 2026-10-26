# Troubleshooting: Bluetooth Not Working or Not Connecting

## Category: Peripherals & Wireless
**Keywords**: bluetooth, pairing, bluetooth audio, headphones, mouse disconnected, bluetooth icon missing

### Possible Causes
1. Bluetooth service disabled in Windows Services (`bthserv`).
2. Bluetooth radio disabled in action center or device manager.
3. Peripheral device battery depleted or in pairing timeout mode.
4. Corrupt Bluetooth radio drivers.
5. Signal interference from metal objects or 2.4 GHz RF transmitters.

### Step-by-Step Troubleshooting Actions

1. **Verify Bluetooth Radio Toggle**:
   - In Windows: Settings > Bluetooth & devices > ensure the main Bluetooth toggle is switched ON.
   - If toggle is missing, verify Flight Mode is off or open Device Manager to see if the adapter is flagged.

2. **Power Cycle Peripheral into Pairing Mode**:
   - Turn off the Bluetooth device (headset, mouse, keyboard) and turn it back on.
   - Press and hold the device's dedicated pairing button until the LED flashes rapidly.

3. **Remove and Re-Pair the Device**:
   - In Settings > Bluetooth & devices > Devices, locate the malfunctioning peripheral, click the three dots, and select "Remove device".
   - Click "Add device" > "Bluetooth" and reconnect.

4. **Restart the Bluetooth Support Windows Service**:
   - Press `Win + R`, type `services.msc`, and press Enter.
   - Locate **Bluetooth Support Service**, right-click, and select "Restart".
   - Ensure Startup Type is set to "Automatic".

5. **Reinstall Bluetooth Driver**:
   - Open Device Manager (`devmgmt.msc`) > expand "Bluetooth".
   - Right-click the primary Bluetooth adapter (e.g. Intel Wireless Bluetooth) > select "Update driver" or "Uninstall device", then restart the PC to trigger auto-reinstallation.

### When to Escalate to IT Admin
- Hardware failure of the integrated motherboard M.2 Wi-Fi/Bluetooth module.
- Enterprise group policy preventing non-approved Bluetooth device pairing.

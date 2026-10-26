# Troubleshooting: Wi-Fi Not Connecting

## Category: Network & Wireless
**Keywords**: wifi, wireless, ssid, disconnect, connection dropped, wlan, network adapter

### Possible Causes
1. Wi-Fi radio or physical hardware switch is toggled off.
2. Airplane mode is active on the operating system.
3. Outdated or corrupted wireless network adapter driver.
4. Cached incorrect Wi-Fi security password or 802.1X certificate error.
5. Router/Access Point IP lease exhaustion or DHCP freeze.
6. IP/TCP configuration conflict or corrupt Winsock catalog.

### Step-by-Step Troubleshooting Actions

1. **Verify Wi-Fi is Enabled**:
   - On Windows: Select the Network icon on the taskbar, verify Wi-Fi is turned ON and Airplane mode is OFF.
   - On macOS: Click the Wi-Fi icon in the menu bar and confirm Wi-Fi is active.

2. **Restart Wireless Adapter**:
   - Open Network Settings > Advanced network settings > Disable the Wi-Fi adapter, wait 10 seconds, then select Enable.

3. **Forget and Reconnect to the Wi-Fi Network**:
   - Go to Wi-Fi Settings > Manage known networks > select your Wi-Fi name > click "Forget".
   - Select the network again, re-enter the network security key, and select Connect.

4. **Power Cycle Local Router/Modem**:
   - If troubleshooting home or small office equipment, unplug the router power cable, wait 30 seconds, and plug it back in. Allow 2 minutes for complete boot.

5. **Flush DNS and Reset TCP/IP Stack**:
   - Open Command Prompt as Administrator and execute safe reset commands:
     ```cmd
     netsh winsock reset
     netsh int ip reset
     ipconfig /release
     ipconfig /renew
     ipconfig /flushdns
     ```
   - Restart the workstation.

### When to Escalate to IT Admin
- If other corporate devices cannot join the access point (infrastructure failure).
- If the Wi-Fi network requires enterprise 802.1X RADIUS authentication or Active Directory domain profile renewal.

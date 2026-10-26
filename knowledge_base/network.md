# Troubleshooting: Network Connectivity Problems (LAN, Ethernet, and IP Conflicts)

## Category: Network Infrastructure
**Keywords**: network, ethernet, ip conflict, 169.254, apipa, default gateway, subnet, lan

### Possible Causes
1. Unplugged, damaged, or crimped RJ-45 Ethernet patch cable.
2. Self-assigned APIPA IP address (`169.254.x.x`) due to DHCP server unreachable.
3. Duplicate IP address conflict with another device on the local network.
4. Faulty switch port, network wall jack, or unmanaged hub.
5. Network adapter power management sleep setting shutting off the NIC.

### Step-by-Step Troubleshooting Actions

1. **Check Physical NIC Activity LEDs**:
   - Inspect the rear Ethernet port on the computer. Ensure the green link LED is solid and amber activity LED is blinking.
   - Reseat both ends of the Ethernet cable firmly until an audible click is heard.

2. **Verify IP Assignment via Command Prompt**:
   - Open Command Prompt and type `ipconfig /all`.
   - If the IPv4 address starts with `169.254.x.x`, your computer failed to receive an IP from the DHCP server (APIPA mode).

3. **Release and Renew DHCP Lease**:
   - In Command Prompt run:
     ```cmd
     ipconfig /release
     ipconfig /renew
     ```
   - Verify that your IPv4 address returns to a valid private subnet (e.g. `192.168.x.x` or `10.x.x.x`).

4. **Disable Energy Efficient Ethernet / Green Ethernet**:
   - Open Device Manager > Network Adapters > right-click Ethernet adapter > Properties > Power Management tab.
   - Uncheck "Allow the computer to turn off this device to save power".

5. **Test Loopback and Default Gateway**:
   - Test internal TCP/IP stack: `ping 127.0.0.1`.
   - Test default gateway: `ping <gateway_ip>`.

### When to Escalate to IT Admin
- Wall data drop or patch panel port disconnected in server rack room.
- Corporate 802.1X Network Access Control (NAC) quarantine isolating workstation.

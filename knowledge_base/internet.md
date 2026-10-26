# Troubleshooting: No Internet Connection (Connected with No Internet)

## Category: Network Connectivity
**Keywords**: no internet, connected without internet, limited access, dns failure, default gateway

### Possible Causes
1. Gateway or ISP connection dropped while local LAN remains active.
2. DNS server failure or unreachable domain nameserver.
3. Static IP misconfiguration or wrong subnet mask.
4. Proxy server or corporate VPN blocking outbound traffic.
5. Firewall or endpoint security isolation rule engaged.

### Step-by-Step Troubleshooting Actions

1. **Verify Physical Cable and Gateway Connectivity**:
   - Check if Ethernet cable link lights are flashing amber/green, or Wi-Fi shows full signal bars with an exclamation mark.
   - Run a ping test to the local default gateway (e.g. `ping 192.168.1.1`). If gateway responds, local link is healthy.

2. **Verify Public IP Ping vs DNS**:
   - Test IP reachability: `ping 8.8.8.8`.
   - If pinging 8.8.8.8 succeeds but opening websites fails, DNS resolution is broken.

3. **Configure Reliable DNS Servers**:
   - Change adapter IPv4 DNS settings to standard public resolvers (Primary: `8.8.8.8`, Secondary: `1.1.1.1`).
   - Run `ipconfig /flushdns` in the command prompt.

4. **Disable Active VPN or Proxy**:
   - Disconnect corporate VPN clients (Cisco AnyConnect, GlobalProtect) temporarily to test if the tunnel stalled.
   - Check Windows Settings > Network & Internet > Proxy > ensure "Automatically detect settings" is enabled and manual proxy is disabled.

5. **Restart Network Stack**:
   - Execute network troubleshooter: Windows Settings > System > Troubleshoot > Other troubleshooters > Network and Internet.

### When to Escalate to IT Admin
- If the entire department or office floor experiences loss of connection.
- If company security policies enforce strict internal DNS and direct public IP routing is disallowed.

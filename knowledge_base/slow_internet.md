# Troubleshooting: Slow Internet Speed & High Latency

## Category: Network Performance
**Keywords**: slow internet, bandwidth, buffering, high ping, packet loss, lag, slow download

### Possible Causes
1. Background cloud file syncs (OneDrive, Google Drive, Dropbox, Windows Update).
2. Network congestion or too many concurrent devices streaming or downloading.
3. Operating on congested 2.4 GHz Wi-Fi instead of 5 GHz or 6 GHz Wi-Fi band.
4. Outdated router firmware or bufferbloat on the ISP modem.
5. Malicious background software or compromised network adapter.

### Step-by-Step Troubleshooting Actions

1. **Conduct a Baseline Speed Test**:
   - Run a speed test (e.g. speedtest.net or fast.com). Compare current speed against your expected service level.

2. **Inspect Background Network Bandwidth**:
   - Open Task Manager (`Ctrl + Shift + Esc`) > select Processes tab > sort by "Network".
   - Identify processes uploading or downloading large volumes (Windows Update, Steam, cloud backups). Pause active syncs.

3. **Switch to 5 GHz Band or Ethernet Cable**:
   - Connect directly to the router via Cat6 Ethernet cable to rule out Wi-Fi radio interference.
   - If using Wi-Fi, ensure connection is made to the `_5G` SSID rather than the `2.4G` band.

4. **Clear Browser Cache and Disable Heavy Extensions**:
   - Clear browser cache, cookies, and temporary data.
   - Disable VPN or proxy services that route traffic through distant geographic nodes.

5. **Restart Router and Workstation**:
   - Power cycle router and restart the PC to release memory and clear congested packet queues.

### When to Escalate to IT Admin
- If corporate office upstream throughput is throttled at the core firewall or gateway SD-WAN.
- If physical cabling in the wall jacks or switches has degraded link speeds (e.g., dropping from 1 Gbps to 100 Mbps).

# Troubleshooting: Computer Running Slowly & System Lag

## Category: Performance & OS Optimization
**Keywords**: slow computer, lag, freeze, high disk usage, high memory, startup apps, 100% cpu

### Possible Causes
1. Excessive startup applications loading simultaneously at system boot.
2. Low free disk space on primary OS drive (Drive C: under 15% free capacity).
3. Insufficient RAM leading to intensive disk paging / swap thrashing.
4. Fragmented or failing mechanical HDD, or background drive indexing loop.
5. Malware, adware, or crypto-mining software running silently.

### Step-by-Step Troubleshooting Actions

1. **Restart the Computer**:
   - Perform a clean reboot: Start > Power > Restart (Fast Startup can hold cached kernel errors across standard shutdowns).

2. **Disable Non-Essential Startup Programs**:
   - Open Task Manager (`Ctrl + Shift + Esc`) > navigate to "Startup apps" tab.
   - Right-click unnecessary heavy items (e.g. Spotify, Teams, Discord, game launchers) and select "Disable".

3. **Free Up Primary Drive Space**:
   - Open Windows Settings > System > Storage.
   - Run "Storage Sense" and delete Temporary Files, previous Windows installations, and empty the Recycle Bin.
   - Ensure Drive C: maintains at least 20-25 GB free space for virtual memory paging.

4. **Check for 100% Disk or Memory Bottlenecks**:
   - In Task Manager > Performance tab, verify if Disk or Memory is pinned at 100%.
   - If Windows Search service is thrashing the drive, temporarily pause search indexing.

5. **Run System File Integrity Check**:
   - Open Command Prompt as Administrator and run:
     ```cmd
     sfc /scannow
     DISM /Online /Cleanup-Image /RestoreHealth
     ```

### When to Escalate to IT Admin
- Hardware upgrades needed (upgrading to SSD or adding physical RAM).
- S.M.A.R.T. disk errors indicating impending storage drive failure.

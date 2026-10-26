# Troubleshooting: Windows Update Failures & Error Codes

## Category: Operating System & Patching
**Keywords**: windows update, update error, 0x80070002, 0x80240034, update stuck, update failed

### Possible Causes
1. Corrupted SoftwareDistribution download cache files.
2. Windows Update service (`wuauserv`) or Background Intelligent Transfer Service (`BITS`) stopped.
3. Insufficient disk space on drive C: to unpack update packages.
4. Third-party antivirus or firewall actively blocking Microsoft CDN endpoints.
5. Missing preliminary servicing stack updates (SSU).

### Step-by-Step Troubleshooting Actions

1. **Run the Built-in Windows Update Troubleshooter**:
   - Open Settings > System > Troubleshoot > Other troubleshooters.
   - Click "Run" next to Windows Update and apply recommended fixes.

2. **Purge the SoftwareDistribution Download Cache**:
   - Open Command Prompt as Administrator and run:
     ```cmd
     net stop wuauserv
     net stop cryptSvc
     net stop bits
     net stop msiserver
     ren C:\Windows\SoftwareDistribution SoftwareDistribution.old
     ren C:\Windows\System32\catroot2 catroot2.old
     net start wuauserv
     net start cryptSvc
     net start bits
     net start msiserver
     ```

3. **Check Free Disk Space**:
   - Windows Feature Updates often require 20-30 GB of contiguous free disk space to stage rollback snapshots. Free up drive space using Disk Cleanup.

4. **Temporarily Disable Third-Party Antivirus & VPN**:
   - Disable non-Microsoft security suites temporarily while attempting the update download.

5. **Perform System Component Store Repair**:
   - Run in Admin Command Prompt:
     ```cmd
     dism /online /cleanup-image /startcomponentcleanup
     sfc /scannow
     ```
   - Reboot and check for updates again.

### When to Escalate to IT Admin
- Enterprise WSUS (Windows Server Update Services) or Microsoft Intune policy synchronization failures.
- In-place OS repair upgrade required for persistent rollback loops.

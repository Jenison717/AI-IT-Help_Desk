# Troubleshooting: Disk and Storage Space Problems

## Category: Storage & File Systems
**Keywords**: disk full, low disk space, drive c, storage sense, temp files, chkdsk, bad sectors

### Possible Causes
1. Accumulation of system temporary files, dump files, and cached updates.
2. Large personal downloads, shadow copies, or oversized video files.
3. Hibernation file (`hiberfil.sys`) or excessive pagefile reservation.
4. File system corruption (NTFS MFT errors or dirty volume bit).
5. Physical bad sectors or failing solid-state drive (SSD) controller.

### Step-by-Step Troubleshooting Actions

1. **Run Built-in Windows Storage Sense**:
   - Open Settings > System > Storage > select "Temporary files".
   - Select "Previous Windows installations", "Delivery Optimization Files", and "Recycle Bin", then click "Remove files".

2. **Identify Oversized Directories**:
   - Check user downloads folder: `C:\Users\<username>\Downloads`. Sort by Size to locate large zip/iso archives.
   - Use Windows built-in TreeSize or Storage breakdown in Windows Settings to pinpoint space hogs.

3. **Compact Hibernation or Disable Fast Startup**:
   - If storage is critically low and laptop is always shut down:
     Open Admin Command Prompt and reduce hibernation size:
     ```cmd
     powercfg /hibernate /size 50
     ```

4. **Verify File System Integrity with CHKDSK**:
   - Open Command Prompt as Administrator and run read-only check:
     ```cmd
     chkdsk C:
     ```
   - If errors are detected, schedule an offline fix: `chkdsk C: /f /r` and reboot.

5. **Clean Component Store with DISM**:
   - Free superseded update backups:
     ```cmd
     dism /online /cleanup-image /startcomponentcleanup /resetbase
     ```

### When to Escalate to IT Admin
- S.M.A.R.T. hardware warnings indicating reallocated sector counts.
- Need to expand virtual disk allocations in VMware/Hyper-V virtual machines.

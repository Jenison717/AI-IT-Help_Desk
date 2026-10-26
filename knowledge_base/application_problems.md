# Troubleshooting: Application Not Opening or Crashing on Launch

## Category: Applications & Software
**Keywords**: app crash, app not opening, application error, stopped working, event id 1000, hang

### Possible Causes
1. Lingering ghost process running in the background locking files or ports.
2. Corrupted user configuration profile or cache directories in `%appdata%`.
3. Incompatible display scaling or GPU hardware acceleration glitch.
4. Missing runtime dynamic link libraries (DLLs).
5. Permission restriction or security software sandboxing.

### Step-by-Step Troubleshooting Actions

1. **Terminate Orphaned Processes in Task Manager**:
   - Press `Ctrl + Shift + Esc` > Details tab.
   - Look for the executable name of the app (e.g. `slack.exe`, `excel.exe`). Right-click and select "End process tree".
   - Try launching the application again.

2. **Clear Application AppData Cache**:
   - Press `Win + R`, type `%localappdata%` or `%appdata%`, and locate the application folder.
   - Rename or delete the `Cache` or `GPUCache` subfolder.

3. **Launch in Safe Mode / Clean State**:
   - For Microsoft Office: hold `Ctrl` while clicking the app shortcut to enter Safe Mode (disabling add-ins).
   - For browsers: test in an Incognito / InPrivate window without extensions.

4. **Run Application Compatibility Troubleshooter**:
   - Right-click the app's desktop icon > Properties > Compatibility tab > check "Run as administrator" or test compatibility mode for Windows 10/8.

5. **Repair or Reinstall Application**:
   - Go to Windows Settings > Apps > Installed apps.
   - Locate the application > click three dots > select "Advanced options" > click "Repair" or "Reset".

### When to Escalate to IT Admin
- Proprietary internal enterprise ERP/CRM software database connectivity failures.
- Application license server disconnection across corporate domain.

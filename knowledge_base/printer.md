# Troubleshooting: Printer Not Working or Print Spooler Errors

## Category: Printing & Hardware
**Keywords**: printer, printing, print spooler, paper jam, offline printer, driver, queue stuck

### Possible Causes
1. Printer is powered off, disconnected from USB, or disconnected from the office Wi-Fi/LAN.
2. Windows Print Spooler service (`spoolsv.exe`) crashed or hung with corrupted queue files.
3. Out-of-paper, paper jam, or empty ink/toner cartridge sensor trigger.
4. "Use Printer Offline" toggle mistakenly checked in Windows.
5. Missing, outdated, or corrupted PCL/PostScript printer driver.

### Step-by-Step Troubleshooting Actions

1. **Verify Physical Hardware State**:
   - Check that printer power LED is solid green/white, paper tray is loaded, and no error codes appear on printer LCD.
   - For USB printers: reconnect cable to a different USB port directly on the PC motherboard.
   - For Network printers: verify the printer display shows a valid IP address on your local subnet.

2. **Clear Stuck Print Queue & Restart Print Spooler**:
   - Open Command Prompt as Administrator and run:
     ```cmd
     net stop spooler
     del /Q /F /S "%systemroot%\System32\Spool\Printers\*.*"
     net start spooler
     ```
   - This purges corrupt spooler cache and re-enables printing.

3. **Disable "Use Printer Offline"**:
   - Open Control Panel > Devices and Printers (or Windows Settings > Printers & scanners).
   - Click the printer > Open print queue > click "Printer" menu in top toolbar.
   - Uncheck "Use Printer Offline" and uncheck "Pause Printing".

4. **Run Windows Printer Troubleshooter**:
   - Go to Settings > System > Troubleshoot > Other troubleshooters > Printer > click "Run".

5. **Reinstall Official Manufacturer Driver**:
   - Remove printer from Settings > Printers & Scanners.
   - Download the clean Universal Print Driver from HP, Canon, Brother, or Epson official support portal and install.

### When to Escalate to IT Admin
- Network print server credentials or Active Directory print deployment group policy issues.
- Mechanical hardware failure (damaged rollers, fuser error, maintenance kit required).

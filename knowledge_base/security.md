# Troubleshooting: Basic Antivirus & Security Troubleshooting

## Category: Security & Endpoint Protection
**Keywords**: antivirus, malware, virus, windows defender, quarantined, trojan, infected, popup, ransomware

### Possible Causes
1. Outdated antivirus security signatures or threat definitions.
2. Suspicious file download or false positive quarantined by endpoint protection (EDR).
3. Rogue browser push notifications displaying fake system alert popups.
4. Active malware payload running in startup registry keys or temp folder.
5. Real-time protection disabled by user or corrupted service.

### Step-by-Step Troubleshooting Actions

1. **Perform an Immediate Full Security Scan**:
   - Open Windows Security > Virus & threat protection.
   - Click "Scan options" > select "Full scan" or "Microsoft Defender Antivirus (offline scan)" > click "Scan now".
   - The offline scan reboots the machine into a clean environment to neutralize rootkits.

2. **Update Security Intelligence Signatures**:
   - In Windows Security > Virus & threat protection updates > click "Check for updates" to download the latest threat definitions.

3. **Check Protection History & Quarantined Items**:
   - Under Virus & threat protection, click "Protection history".
   - Review detected items. If a verified business file was blocked as a false positive, do not restore it without IT security sign-off.

4. **Disable Fraudulent Browser Notifications**:
   - If seeing continuous fake "Your PC is Infected! Call 1-800-XXX" popups, open Chrome/Edge settings > Privacy & security > Site settings > Notifications.
   - Remove permission for any unfamiliar websites to send push notifications.

5. **Isolate Device from Network if Active Compromise Suspected**:
   - If ransomware or active remote intruder is observed: immediately disconnect the Ethernet cable and disable Wi-Fi to stop lateral spread across the corporate network.

### When to Escalate to IT Admin (CRITICAL)
- If ransomware note is displayed or files are being encrypted.
- If corporate EDR (CrowdStrike, SentinelOne, Defender for Endpoint) alerts on credential dumping or lateral movement.

# Troubleshooting: Software Installation Problems

## Category: Software & Deployment
**Keywords**: install error, software install failed, administrator permission, msi error, installer stuck

### Possible Causes
1. Lack of local administrator privileges (UAC elevation denied).
2. Existing installation in progress or corrupted Windows Installer service (`msiserver`).
3. Corrupted or incomplete download of installer package.
4. Missing runtime dependencies (Microsoft Visual C++ Redistributable, .NET Framework).
5. Antivirus heuristic blocking installer execution or quarantining temporary setup files.

### Step-by-Step Troubleshooting Actions

1. **Run Installer as Administrator**:
   - Right-click the `.exe` or `.msi` setup file and select "Run as administrator".
   - If prompted for IT credentials on a domain machine, contact the helpdesk for remote credential injection.

2. **Verify Windows Installer Service is Running**:
   - Press `Win + R`, type `services.msc`, locate "Windows Installer".
   - If stopped, right-click and choose "Start".

3. **Install Required Visual C++ and .NET Prerequisites**:
   - Verify if the application demands Visual C++ Redistributable (2015-2022) or .NET Desktop Runtime 6.0/8.0. Download and install standard prerequisites from Microsoft.

4. **Clean Windows Temp Folder**:
   - Press `Win + R`, type `%temp%`, press Enter, and delete temporary setup cache files that could lock the installer.

5. **Re-Download Installer & Verify Checksum**:
   - Download a fresh copy of the installer directly from the official software vendor portal.

### When to Escalate to IT Admin
- Software requires corporate license activation keys, Active Directory group deployment, or administrative elevation approval.

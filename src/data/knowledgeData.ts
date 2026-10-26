export interface KnowledgeDoc {
  id: string;
  filename: string;
  title: string;
  category: string;
  keywords: string[];
  causes: string[];
  steps: string[];
  escalation: string;
}

export const KNOWLEDGE_DOCS: KnowledgeDoc[] = [
  {
    id: "wifi",
    filename: "wifi.md",
    title: "Wi-Fi Not Connecting",
    category: "Network & Wireless",
    keywords: ["wifi", "wireless", "ssid", "disconnect", "wlan", "network adapter"],
    causes: [
      "Wi-Fi radio or physical hardware switch is toggled off.",
      "Airplane mode is active on the operating system.",
      "Outdated or corrupted wireless network adapter driver.",
      "Router/Access Point IP lease exhaustion or DHCP freeze."
    ],
    steps: [
      "Verify Wi-Fi is enabled and Airplane mode is turned off in the taskbar or menu bar.",
      "Restart the wireless adapter via Network Settings > Disable, wait 10 seconds, then Enable.",
      "Forget the Wi-Fi network in Manage Known Networks, then reconnect and enter security key.",
      "Power cycle the local router/modem by unplugging power for 30 seconds and rebooting.",
      "Open Command Prompt as Admin and execute: netsh winsock reset && netsh int ip reset && ipconfig /flushdns"
    ],
    escalation: "Escalate to network admin if other corporate devices cannot join or if 802.1X RADIUS authentication fails."
  },
  {
    id: "internet",
    filename: "internet.md",
    title: "No Internet Connection (Connected with No Internet)",
    category: "Network Connectivity",
    keywords: ["no internet", "limited access", "dns failure", "default gateway", "connected without internet"],
    causes: [
      "Gateway or ISP connection dropped while local LAN remains active.",
      "DNS server failure or unreachable domain nameserver.",
      "Static IP misconfiguration or proxy server blocking outbound traffic."
    ],
    steps: [
      "Verify Ethernet cable link lights or Wi-Fi signal strength and ping default gateway (192.168.1.1).",
      "Test IP reachability by pinging public IP (8.8.8.8) to distinguish DNS failure from physical link failure.",
      "Configure reliable public DNS servers (Primary: 8.8.8.8, Secondary: 1.1.1.1) and run ipconfig /flushdns.",
      "Temporarily disconnect corporate VPN clients and check Proxy settings to ensure manual proxy is disabled.",
      "Run the Windows Network and Internet Troubleshooter to reset the adapter stack."
    ],
    escalation: "Escalate if entire department loses connectivity or corporate proxy enforces mandatory certificate."
  },
  {
    id: "slow_internet",
    filename: "slow_internet.md",
    title: "Slow Internet Speed & High Latency",
    category: "Network Performance",
    keywords: ["slow internet", "bandwidth", "buffering", "high ping", "packet loss", "lag"],
    causes: [
      "Background cloud sync (OneDrive, Google Drive, Windows Update) consuming bandwidth.",
      "Operating on congested 2.4 GHz Wi-Fi band instead of 5 GHz / 6 GHz band.",
      "Network congestion or high latency on ISP modem/bufferbloat."
    ],
    steps: [
      "Run a baseline speed test at fast.com or speedtest.net to compare against expected throughput.",
      "Open Task Manager (Ctrl + Shift + Esc), sort by Network, and pause heavy background uploads.",
      "Switch connection from 2.4 GHz Wi-Fi to 5 GHz SSID or plug in a Cat6 Ethernet cable.",
      "Clear browser cache, cookies, and disable bandwidth-heavy browser extensions.",
      "Power cycle the router and reboot workstation to clear congested packet buffers."
    ],
    escalation: "Escalate if corporate firewall throttles throughput or wall Ethernet drop negotiates at 100 Mbps instead of 1 Gbps."
  },
  {
    id: "printer",
    filename: "printer.md",
    title: "Printer Not Working or Print Spooler Errors",
    category: "Printing & Hardware",
    keywords: ["printer", "printing", "print spooler", "paper jam", "offline printer", "queue stuck"],
    causes: [
      "Printer is offline, powered off, or disconnected from USB/LAN.",
      "Windows Print Spooler service hung with corrupted queue files.",
      "'Use Printer Offline' toggle inadvertently enabled in Windows."
    ],
    steps: [
      "Verify printer power LED is solid and check for physical paper jams or out-of-paper indicators.",
      "Restart Print Spooler service and clear stuck queue in Admin CMD: net stop spooler && del /Q /F /S \"%systemroot%\\System32\\Spool\\Printers\\*.*\" && net start spooler.",
      "Open printer queue from Settings, click 'Printer' menu, and uncheck 'Use Printer Offline'.",
      "Run the built-in Windows Printer Troubleshooter.",
      "Download and install the latest official manufacturer Universal Print Driver."
    ],
    escalation: "Escalate for print server permission errors, Active Directory group deployment, or hardware roller failures."
  },
  {
    id: "overheating",
    filename: "overheating.md",
    title: "Laptop Overheating & Loud Cooling Fans",
    category: "Hardware & Thermal",
    keywords: ["overheating", "hot laptop", "fan noise", "throttling", "thermal shutdown", "vents blocked"],
    causes: [
      "Cooling vents and heatsink grilles blocked by accumulated dust or lint.",
      "Operating on soft surfaces (bed, blanket, lap) blocking air intake.",
      "Runaway background CPU/GPU loop processes consuming 100% processor capacity."
    ],
    steps: [
      "Move the laptop to a hard, flat, elevated surface or laptop cooling stand.",
      "Open Task Manager (Ctrl + Shift + Esc), sort by CPU, and terminate any rogue background tasks.",
      "Power off laptop, unplug AC power, and blow short bursts of compressed air through cooling vents.",
      "Set Windows Power Mode to 'Balanced' or 'Best power efficiency'.",
      "Check manufacturer support app (Dell Command, Lenovo Vantage, HP Support Assistant) for BIOS thermal updates."
    ],
    escalation: "Escalate immediately if laptop shuts down with thermal emergency or fan emits grinding/squealing sounds."
  },
  {
    id: "slow_computer",
    filename: "slow_computer.md",
    title: "Computer Running Slowly & System Lag",
    category: "Performance & OS",
    keywords: ["slow computer", "lag", "freeze", "high disk usage", "high memory", "startup apps"],
    causes: [
      "Excessive startup apps loading simultaneously on boot.",
      "Low free disk space on Drive C: (under 15% free headroom).",
      "High RAM utilization causing virtual memory swap thrashing."
    ],
    steps: [
      "Perform a clean reboot via Start > Power > Restart to clear cached kernel state.",
      "Open Task Manager > Startup Apps tab and disable non-essential launchers (Spotify, Discord, Teams).",
      "Run Storage Sense to clean temporary files, previous Windows installations, and empty the Recycle Bin.",
      "Check Task Manager Performance tab to verify if Disk or Memory is pegged at 100%.",
      "Run system integrity repair in Admin CMD: sfc /scannow && DISM /Online /Cleanup-Image /RestoreHealth."
    ],
    escalation: "Escalate for hardware RAM/SSD upgrades or when S.M.A.R.T. disk telemetry signals hardware drive failure."
  },
  {
    id: "bluetooth",
    filename: "bluetooth.md",
    title: "Bluetooth Not Working or Pairing Failure",
    category: "Peripherals & Wireless",
    keywords: ["bluetooth", "pairing", "headphones", "mouse disconnected", "bluetooth icon missing"],
    causes: [
      "Bluetooth service disabled or peripheral battery drained.",
      "Corrupted Bluetooth adapter driver in Device Manager.",
      "Signal interference or device in pairing timeout mode."
    ],
    steps: [
      "Verify Bluetooth toggle is switched ON in Windows Settings > Bluetooth & Devices.",
      "Power cycle peripheral into pairing mode by holding pairing button until LED flashes rapidly.",
      "Remove device from Bluetooth settings, click 'Add device', and pair freshly.",
      "Restart 'Bluetooth Support Service' via services.msc and set Startup Type to Automatic.",
      "Reinstall Bluetooth adapter driver in Device Manager (devmgmt.msc)."
    ],
    escalation: "Escalate if integrated motherboard M.2 Bluetooth card has hardware failure or enterprise GPO disables pairing."
  },
  {
    id: "keyboard",
    filename: "keyboard.md",
    title: "Keyboard Unresponsive or Repeating Keys",
    category: "Input Devices",
    keywords: ["keyboard", "typing", "keys not working", "sticky keys", "repeating letters"],
    causes: [
      "Windows Filter Keys or Sticky Keys accessibility options active.",
      "Physical debris under mechanical switch or low battery on wireless keyboard.",
      "Incorrect keyboard language input layout selected (e.g., AZERTY vs QWERTY)."
    ],
    steps: [
      "Test typing in Notepad to isolate whether problem is system-wide or isolated to one program.",
      "Disable Filter Keys and Sticky Keys in Settings > Accessibility > Keyboard.",
      "Verify keyboard language on the taskbar (press Windows Key + Spacebar to reset to US).",
      "Reinstall keyboard driver in Device Manager and reboot workstation.",
      "Test keyboard on a different USB 3.0 port or replace wireless batteries."
    ],
    escalation: "Escalate for laptop internal ribbon cable failure or hardware matrix defect."
  },
  {
    id: "mouse",
    filename: "mouse.md",
    title: "Mouse Cursor Freezing or Jumping",
    category: "Input Devices",
    keywords: ["mouse", "cursor", "trackpad", "pointer stuck", "double click", "optical sensor"],
    causes: [
      "Optical sensor blocked by dust or used on reflective glass surface.",
      "Low battery or wireless RF interference.",
      "Touchpad disabled via Fn hotkey toggle on laptop."
    ],
    steps: [
      "Clean optical lens with compressed air and use an opaque, dark cloth mousepad.",
      "Replace wireless batteries and plug USB receiver into an unblocked USB port.",
      "For laptop users: verify touchpad toggle hotkey (Fn + F7/F9) or toggle on in Settings.",
      "Adjust pointer precision speed in Mouse Settings and disable 'Enhance pointer precision'.",
      "Uninstall mouse driver in Device Manager and restart computer."
    ],
    escalation: "Escalate for internal microswitch failure causing phantom double-clicks or trackpad physical defects."
  },
  {
    id: "windows_update",
    filename: "windows_update.md",
    title: "Windows Update Failures & Error Codes",
    category: "Operating System",
    keywords: ["windows update", "update error", "0x80070002", "update stuck", "update failed"],
    causes: [
      "Corrupted SoftwareDistribution update download cache.",
      "Windows Update service or BITS stopped.",
      "Insufficient free disk space on Drive C:."
    ],
    steps: [
      "Run the built-in Windows Update Troubleshooter in Settings > System > Troubleshoot.",
      "Stop update services and purge download cache: net stop wuauserv && ren C:\\Windows\\SoftwareDistribution SoftwareDistribution.old && net start wuauserv.",
      "Ensure at least 25 GB free disk space on Drive C: for staging update snapshots.",
      "Temporarily disable third-party antivirus suites that intercept Microsoft CDN traffic.",
      "Run component store cleanup: dism /online /cleanup-image /startcomponentcleanup && sfc /scannow."
    ],
    escalation: "Escalate for corporate WSUS / Intune synchronization errors or recurring Blue Screen rollbacks."
  },
  {
    id: "software_installation",
    filename: "software_installation.md",
    title: "Software Installation Failures & MSI Errors",
    category: "Software Deployment",
    keywords: ["install error", "software install failed", "administrator permission", "msi error"],
    causes: [
      "Lack of local administrator privileges (UAC elevation denied).",
      "Corrupted Windows Installer service (msiserver) or existing install in progress.",
      "Missing Microsoft Visual C++ or .NET Framework runtime prerequisites."
    ],
    steps: [
      "Right-click the setup file and select 'Run as administrator'.",
      "Ensure Windows Installer service is running in services.msc.",
      "Install required Visual C++ Redistributable (2015-2022) and .NET Desktop Runtime from Microsoft.",
      "Clear temporary installer files by emptying %temp% directory.",
      "Re-download setup package directly from official vendor website."
    ],
    escalation: "Escalate if corporate policy blocks software or software requires Active Directory software push."
  },
  {
    id: "application_problems",
    filename: "application_problems.md",
    title: "Application Not Opening or Crashing on Launch",
    category: "Applications",
    keywords: ["app crash", "app not opening", "stopped working", "hang", "event id 1000"],
    causes: [
      "Ghost process running in background locking configuration files.",
      "Corrupted cache directory in %appdata% or %localappdata%.",
      "Incompatible GPU hardware acceleration or display scaling."
    ],
    steps: [
      "Open Task Manager Details tab, locate the process name, and select 'End process tree'.",
      "Press Win + R, type %localappdata%, locate application folder, and clear its Cache subfolder.",
      "Launch application in Safe Mode (e.g., hold Ctrl while launching Microsoft Office apps).",
      "Run Application Compatibility Troubleshooter via right-click Properties.",
      "Use Windows Settings > Apps > Installed apps to select 'Repair' or 'Reset'."
    ],
    escalation: "Escalate if internal enterprise ERP/CRM database link is severed or license server is unreachable."
  },
  {
    id: "login_problems",
    filename: "login_problems.md",
    title: "Password and Account Login Problems",
    category: "Identity & Access",
    keywords: ["password", "login", "locked out", "reset password", "mfa", "authenticator"],
    causes: [
      "Caps Lock or Num Lock toggled unintentionally.",
      "Account locked out from consecutive bad attempts.",
      "Multi-Factor Authentication (MFA) time-drift desynchronization."
    ],
    steps: [
      "Click the eye icon to verify password casing and confirm keyboard layout.",
      "Access self-service password reset portal (passwordreset.microsoftonline.com).",
      "For MFA issues: ensure smartphone date/time is set to 'Automatic' to prevent TOTP code drift.",
      "Open Windows Credential Manager and remove stale stored credentials for the account.",
      "Wait 15-30 minutes for automated domain security lockout timers to reset."
    ],
    escalation: "Escalate to domain administrator for manual account unlock or replacement of lost MFA security keys."
  },
  {
    id: "email",
    filename: "email.md",
    title: "Email Problems (Outlook Disconnected / Not Receiving)",
    category: "Communication",
    keywords: ["email", "outlook", "inbox", "not receiving", "outlook disconnected", "exchange"],
    causes: [
      "Outlook toggled to 'Work Offline' mode.",
      "Mailbox quota reached (100% capacity full).",
      "Corrupted Outlook local offline cache file (.ost)."
    ],
    steps: [
      "Log into Webmail browser portal to confirm whether exchange servers and credentials work.",
      "In Outlook: click 'Send / Receive' tab and uncheck 'Work Offline' if highlighted.",
      "Inspect Outbox folder for oversized emails (30+ MB attachments) and delete or move them.",
      "Launch Outlook in Safe Mode via outlook.exe /safe to isolate faulty third-party COM add-ins.",
      "Close Outlook, rename .ost file in %localappdata%\\Microsoft\\Outlook, and restart to rebuild cache."
    ],
    escalation: "Escalate for organization-wide MX/DNS record outages or 550 SPF/DKIM policy rejections."
  },
  {
    id: "network",
    filename: "network.md",
    title: "LAN, Ethernet, and IP Conflict Problems",
    category: "Network Infrastructure",
    keywords: ["network", "ethernet", "ip conflict", "169.254", "apipa", "lan"],
    causes: [
      "Damaged or unplugged RJ-45 Ethernet cable.",
      "Self-assigned APIPA IP address (169.254.x.x) due to unreachable DHCP server.",
      "Duplicate IP address conflict with another host on local subnet."
    ],
    steps: [
      "Inspect rear NIC link LEDs (solid green link, flashing amber activity) and reseat cable firmly.",
      "Run ipconfig /all in Command Prompt to check if IPv4 is stuck on 169.254.x.x.",
      "Execute ipconfig /release followed by ipconfig /renew to fetch fresh DHCP lease.",
      "Disable Energy Efficient Ethernet in NIC Device Manager Power Management properties.",
      "Ping loopback (127.0.0.1) and default gateway to verify physical adapter functionality."
    ],
    escalation: "Escalate for severed patch panel connections in server room or 802.1X NAC quarantine."
  },
  {
    id: "security",
    filename: "security.md",
    title: "Antivirus, Malware & Browser Hijacking",
    category: "Security & Antivirus",
    keywords: ["antivirus", "malware", "virus", "windows defender", "quarantined", "trojan", "popup"],
    causes: [
      "Outdated antivirus threat definitions.",
      "Fraudulent browser push notifications mimicking system popups.",
      "Malware payload quarantined or running in temporary directories."
    ],
    steps: [
      "Launch Windows Security > Virus & Threat Protection and execute a Full Scan or Offline Scan.",
      "Click 'Check for updates' under Security Intelligence to download current definitions.",
      "Review Protection History for quarantined files before taking action.",
      "Remove notification permissions for unknown websites in Chrome/Edge Settings > Privacy > Notifications.",
      "If ransomware or active intrusion is suspected: IMMEDIATELY disconnect Ethernet and disable Wi-Fi."
    ],
    escalation: "CRITICAL: Escalate immediately to IT Security if ransomware notes appear or endpoint EDR alerts."
  },
  {
    id: "storage",
    filename: "storage.md",
    title: "Disk & Low Storage Space Problems",
    category: "Storage",
    keywords: ["disk full", "low disk space", "drive c", "storage sense", "temp files", "chkdsk"],
    causes: [
      "Accumulated Windows update staging files, memory dumps, and temp caches.",
      "Large downloads or oversized video files in user profile folders.",
      "Corrupted NTFS file system master file table entries."
    ],
    steps: [
      "Open Settings > System > Storage > Temporary Files and click 'Remove files'.",
      "Inspect Downloads folder (C:\\Users\\<username>\\Downloads) and archive or delete large ZIP/ISO files.",
      "Compact hibernation footprint in Admin CMD: powercfg /hibernate /size 50.",
      "Run read-only chkdsk C: in Command Prompt to inspect file system health.",
      "Clean superseded updates: dism /online /cleanup-image /startcomponentcleanup /resetbase."
    ],
    escalation: "Escalate for disk sector reallocations (failing drive) or to expand virtual disk size in VMs."
  },
  {
    id: "usb",
    filename: "usb.md",
    title: "USB Device Not Detected or Code 43 Error",
    category: "Hardware & Peripherals",
    keywords: ["usb", "flash drive", "external hard drive", "code 43", "device descriptor failure"],
    causes: [
      "USB selective suspend feature shutting off power to root hub.",
      "Corrupted USB controller drivers or loose front-case header cable.",
      "Drive missing an assigned drive letter in Disk Management."
    ],
    steps: [
      "Plug device directly into rear motherboard USB 3.0 port instead of front case ports or passive hubs.",
      "Open Disk Management (Win + X), right-click volume, and choose 'Change Drive Letter and Paths'.",
      "In Device Manager: expand USB controllers, right-click flagged device, and choose 'Uninstall device', then scan for hardware changes.",
      "Disable USB selective suspend in Windows Power Options > Advanced Settings.",
      "Test device on a secondary PC to determine if peripheral or host port is defective."
    ],
    escalation: "Escalate for corporate USB storage block policy (BitLocker-to-Go / DLP) or damaged physical motherboard pins."
  }
];

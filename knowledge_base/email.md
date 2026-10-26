# Troubleshooting: Email Problems (Outlook, Exchange, and IMAP/SMTP)

## Category: Messaging & Communication
**Keywords**: email, outlook, inbox, not receiving email, bounce back, outlook disconnected, exchange, smtp

### Possible Causes
1. Mailbox quota or mailbox storage capacity exceeded (100% full).
2. Outlook stuck in "Work Offline" mode or status bar indicates "Disconnected".
3. Corrupted Outlook local cache file (`.ost` or `.pst`).
4. Incorrect incoming/outgoing mail server ports or SSL/TLS encryption requirements.
5. Large stuck outgoing email with oversize attachment in Outbox.

### Step-by-Step Troubleshooting Actions

1. **Verify Mailbox Quota in Webmail**:
   - Log in to Webmail (e.g. Outlook on the Web via browser).
   - If webmail works, the issue is restricted to the desktop client. Check mailbox storage size under Settings > Storage.

2. **Check Outlook "Work Offline" Status**:
   - In Microsoft Outlook: select the "Send / Receive" tab at the top.
   - Look at "Work Offline". If highlighted, click it once to toggle back to Online mode.
   - Check the bottom right status bar: it should display "Connected to: Microsoft Exchange".

3. **Purge Stuck Outbox Messages**:
   - Click the "Outbox" folder. If an email with a 30+ MB attachment is stuck in sending queue, click "Send / Receive" > "Work Offline", restart Outlook, delete or move the stuck email, and return online.

4. **Launch Outlook in Safe Mode**:
   - Press `Win + R`, type `outlook.exe /safe`, and press Enter.
   - If Outlook opens normally without hanging, disable offending third-party add-ins (File > Options > Add-ins > COM Add-ins > Go).

5. **Rebuild Corrupted Outlook OST Profile**:
   - Close Outlook. Open Control Panel > Mail > Data Files > select Open File Location.
   - Rename `username.ost` to `username.ost.old`.
   - Start Outlook; it will automatically re-download a pristine offline cache from the Exchange server.

### When to Escalate to IT Admin
- Domain MX or DNS records changed, causing organization-wide mail delivery failure.
- Email rejected with 550 SPF, DKIM, or DMARC security policy errors.

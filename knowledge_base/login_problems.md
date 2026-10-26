# Troubleshooting: Password and Login Problems

## Category: Identity & Access Management
**Keywords**: password, login, locked out, reset password, mfa, authenticator, credentials, kerberos

### Possible Causes
1. Caps Lock or Num Lock toggled unintentionally during entry.
2. Account locked out due to multiple consecutive invalid password attempts.
3. Multi-Factor Authentication (MFA/2FA) token out of sync or mobile push notification not delivered.
4. Expired enterprise Active Directory domain password.
5. Cached stale credentials in Windows Credential Manager.

### Step-by-Step Troubleshooting Actions

1. **Verify Caps Lock and Keyboard Layout**:
   - Click the "eye" preview icon on the password input field to inspect typed characters for casing or punctuation errors.
   - Confirm language layout (US vs UK keyboard alters punctuation locations).

2. **Check for Self-Service Password Reset (SSPR)**:
   - Click "Forgot My Password" or visit your company's self-service password reset portal (e.g. `passwordreset.microsoftonline.com`).
   - Authenticate with your secondary phone or recovery email.

3. **Multi-Factor Authentication (MFA) Troubleshooting**:
   - Ensure the mobile phone date and time are set to "Automatic", as time-drift breaks TOTP 6-digit codes.
   - Switch from push notification to SMS code or manual 6-digit code in Microsoft Authenticator or Google Authenticator.

4. **Purge Stale Credentials in Windows Credential Manager**:
   - Open Start > type "Credential Manager" > select "Windows Credentials".
   - Under "Generic Credentials", locate entries for the affected service and click "Remove".
   - Restart the application and input fresh credentials.

5. **Wait Out Account Lockout Window**:
   - Standard security policy automatically unlocks accounts after 15 or 30 minutes.

### When to Escalate to IT Admin
- If account is locked in Active Directory / Azure Entra ID and requires admin unlock.
- MFA device lost, damaged, or wiped, requiring admin token reset.

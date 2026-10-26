# Troubleshooting: Keyboard Problems (Unresponsive or Repeating Keys)

## Category: Input Devices & Hardware
**Keywords**: keyboard, typing, keys not working, sticky keys, repeating letters, mechanical keyboard

### Possible Causes
1. Physical debris, dust, or liquid spill under key switches.
2. Windows Filter Keys or Sticky Keys accessibility options inadvertently enabled.
3. Outdated or conflicting HID keyboard driver.
4. USB port power fluctuation or wireless receiver RF interference.
5. Wrong keyboard language layout selected (e.g. AZERTY instead of QWERTY).

### Step-by-Step Troubleshooting Actions

1. **Test in Another Application or Safe Mode**:
   - Open Notepad and test every key.
   - If keys work in Notepad but not a specific application, the issue is software-specific.

2. **Disable Filter Keys and Sticky Keys**:
   - Press Windows Settings > Accessibility > Keyboard.
   - Ensure "Sticky keys" and "Filter keys" toggles are turned OFF (Filter keys ignores repeated keystrokes).

3. **Check Keyboard Input Language**:
   - Look at the taskbar language indicator next to the clock (e.g., `ENG US`).
   - Press `Windows Key + Spacebar` to switch back to the correct regional input language.

4. **Reinstall Keyboard Drivers in Device Manager**:
   - Press `Win + X` > select Device Manager.
   - Expand "Keyboards" > right-click "Standard PS/2 Keyboard" or "HID Keyboard Device" > choose "Uninstall device".
   - Restart the computer. Windows will re-detect and reinstall clean drivers automatically.

5. **Hardware Isolation**:
   - Plug the keyboard into a different USB port (preferably a rear USB 3.0 port).
   - If wireless, replace AA/AAA batteries and relocate the 2.4 GHz USB dongle away from heavy USB 3.0 hubs.

### When to Escalate to IT Admin
- Laptop built-in internal ribbon cable disconnect or hardware keyboard matrix failure requiring chassis replacement.

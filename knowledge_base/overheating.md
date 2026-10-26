# Troubleshooting: Laptop Overheating & Loud Cooling Fans

## Category: Hardware & Thermal Management
**Keywords**: overheating, hot laptop, fan noise, throttling, thermal shutdown, vents blocked, temperature

### Possible Causes
1. Cooling air vents and heatsink blocked by dust, hair, or lint.
2. Operating on soft surfaces (bed, pillow, blanket, lap) suffocating intake vents.
3. Heavy background CPU/GPU tasks (mining, rogue loop processes, antivirus indexing).
4. Dried or deteriorated thermal paste between CPU and cooling heatsink pipes.
5. Obsolete BIOS thermal management curves or failed cooling fan bearings.

### Step-by-Step Troubleshooting Actions

1. **Clear Air Intakes and Elevate Chassis**:
   - Move laptop to a hard, flat, elevated surface (e.g. wooden desk or laptop riser stand).
   - Never use the laptop on top of fabric, bedsheets, or couches where vents are blocked.

2. **Inspect & Terminate Runaway CPU Processes**:
   - Press `Ctrl + Shift + Esc` to open Task Manager.
   - Click "CPU" column to sort highest consumers. If an unexpected background utility consumes 80-100% CPU, right-click and select "End task".

3. **Clean Vents with Compressed Air**:
   - Power down the laptop and unplug the AC power adapter.
   - Use short, gentle bursts of compressed air through exhaust and intake grilles to dislodge accumulated dust.

4. **Adjust Windows Power Mode to Balanced or Efficiency**:
   - Go to Settings > System > Power & battery > set "Power mode" to "Balanced" or "Best power efficiency".
   - Under Advanced Power Options > Processor power management > set "Maximum processor state" to 95% on AC power to curb aggressive boost temperatures.

5. **Update BIOS and Chipset Drivers**:
   - Check the laptop manufacturer's management app (Dell Command, Lenovo Vantage, HP Support Assistant) for critical BIOS thermal updates.

### When to Escalate to IT Admin
- If laptop shuts down abruptly with thermal emergency warnings.
- Fan produces grinding, rattling, or squealing noises (bearing failure).
- Re-pasting the CPU/GPU with fresh thermal paste is required.

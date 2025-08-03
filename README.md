# fj-lcnc-cfg
This is a snapshot of key configuration files for my personal LinuxCNC installation, which may serve as an example for others looking to integrate a similar machine and/or features.

Presently I'm running LinuxCNC v2.9.4 installed from the official ISO.

What's included:
* Machine config files
* M6 remap
  * Automatic tool changes with actuated linear tool rack
  * Tool length measurement with tool setter
* Modifications to the qtdragon UI
* HAL components for VFD and air compressor control
* Actuated dust shoe control (with automatic retract during tool changes)

## Other dependencies:
You need to create a python virtual environment in ```/usr/local/venv/linuxcnc_venv``` and install dependencies via requirements.txt.  This was required due to Debian 12 locking down python package management, and the adafruit-io library not being available via apt.

## Configuration Description
The following are key details about my CNC machine, to give context to this overall configuration.
* Gantry-style CNC router with dual Y drive motors
    * XYYZ config (Joints: X=0, YL=1, YR=2, Z=3)
* Inductive proximity homing/limit switches
    * Z+ home/limit
    * X (single sensor mounted on X carriage covers X+ home/limit and X- limit)
    * Y+ home/limit (separate sensors Left and Right for independent homing of either side of the gantry)
    * Y- limit (right side only)
* Homing config
    * Machine homes in the positive direction for all axes (home is in the top/back/right corner)
    * Z homes first (for clearance)
    * YL and YR home independently - but coordinated to eliminate any racking of the gantry
    * X homes coordinated with YL and YR - not out of necessity, but it saves time relative to homing sequentially
* Clearpath SDSK integrated servos - step and direction control, open-loop as far as LinuxCNC is concerned
* Mesa 7i93 ethernet FPGA controller
    * Custom breakout board interfaces Clearpath servos, limit switches, hardware E-stops, probes, tool setter, and miscellaneous other I/O
    * 7i37-COM I/O card for additional I/O (e.g. Solenoid valves for ATC spindle)
    * Modified HOSTMOT2 FW to support these breakout boards
* Dual probe inputs:
    * Touch plate (electrical continuity type) for zeroing Z work coordinate to the workpiece (Normally Open)
    * 3D touch probe for other probing operations (Normally Closed)
* ATC spindle and linear tool rack (oriented along X axis) - the rack is actuated with air cylinders, extending for tool changes and retracting out of the way otherwise
* M6 remapped for both manual and automatic tool changes, with automatic tool length offset using tool setter.  This was achieved using an NGC script as the top-level remap, which calls custom M-code (M102) which invokes a python script when necessary to generate a user prompt.  A button on the GUI toggles between manual and automatic tool changes.
    * In Manual tool change mode, the machine moves to a convenient location and prompts the user to change the tool.  
    * In Automatic tool change mode, the machine changes the tool automatically (of course) - [Example](https://www.youtube.com/watch?v=98X_LPUHFn0 "ATC example video") (Actuated tool rack was added after this video)
    * Following tool change, the machine moves over the tool setter (fixed location on machine bed)
    * The tool length offset is measured with zero work offset (using G59.3) and therefore the measured tool length offset is equivalent to the absolute Z position in machine coordinates at the point where the tool contacted the setter.
        * TLO value is always negative
        * TLO is independent of active work coordinate offsets (e.g. G54)
* Hitachi WJ200 VFD controlled via Modbus using USB-RS485 adapter 
* iMach P4S pendant
* Automatically turn on air compressor (MQTT via Adafruit.io, custom ESP32-based hardware controls compressor)

## qtdragon gui
I started with the stock qtdragon UI and made a few changes:
* Resized to best fit my 1600x1200 display
* Added some indicators & controls in the lower right for tool changer-related items (tool pocket sensors, compressed air pressure sensor, auto/manual tool change mode)
* Added some ATC-related buttons to the left pane of the tool tab
* Added dust shoe controls center right
<img width="665" height="467" alt="image" src="https://github.com/user-attachments/assets/966364ed-c023-435a-ba7c-0505c47945c8" />

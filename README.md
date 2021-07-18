# fj-lcnc-cfg
This is a snapshot of key configuration files for my personal LinuxCNC installation, which may serve as an example for others looking to integrate a similar machine and/or features.

Presently I'm running the v2.8.2 release - I can't confirm whether these files will be compatible with other versions.

What's included:
* Machine config files
* M6 remap
* Modifications to the qtdragon UI

## Structure
The following assumes a typical LinuxCNC install, such as if you installed from an official ISO:
* `configs` and `nc_files` correspond to the equivalent subdirectories within /home/<username>/linuxcnc/
* 'qtvcp' corresponds to /usr/share/qtvcp

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
    * 7i37-COM I/O card for additional I/O (not currently in use)
	* Modified HOSTMOT2 FW to support these breakout boards
* Touch plate (electrical continuity type) for zeroing Z work coordinate to the workpiece
* 3D touch probe for other probing operations
* M6 remapped for manual tool changes with automatic tool length offset using tool setter.  This was achieved using an NGC script as the top-level remap, which calls custom M-code (M102) which invokes a python script when necessary to generate a user prompt.
    * On M6, the machine moves to a convenient location and prompts the user to change the tool.  
	* Upon clicking OK, the machine moves over the tool setter (fixed location on machine bed)
	* Spindle runs counterclockwise at low RPM during probe move to reduce variation based on uncontrolled tool orientation
	* The tool length offset is measured with zero work offset (using G59.3) and therefore the measured tool length offset is equivalent to the absolute Z position in machine coordinates at the point where the tool contacted the setter.
	    * TLO value is always negative
		* TLO is independent of active work coordinate offsets (e.g. G54)
	* There is risk of ending up with a bad Z offset in the event that the operator sets a WCS Z offset **prior** to measuring/setting the tool length offset (via M6).  To help mitigate this, when M6 is called with no tool yet loaded (current tool = 0), a warning dialog comes up giving the operator a few options for how to proceed.
* Hitachi WJ200 VFD controlled via Modbus using USB-RS485 adapter 
* iMach P4S pendant

@echo off
REM --- Configuration Variables ---
SET WiresharkPath="C:\Users\vcatstester\Desktop\WiresharkPortable64\App\Wireshark\tshark.exe"
REM Replace 'Ethernet' with your actual interface name or number (e.g., '3' or 'Ethernet Adapter Ethernet 5')
SET Interface="VCU" 
SET LogFolder="C:\Users\vcatstester\Desktop\Wireshark_Logging"
REM Filter for DoIP traffic (ISO 13400) SET CaptureFilter="doip" 
SET FileName=DoIP_Capture_%DATE:~10,4%-%DATE:~4,2%-%DATE:~7,2%_%TIME:~0,2%-%TIME:~3,2%-%TIME:~6,2%.pcapng

REM Ensure the log folder exists
IF NOT EXIST %LogFolder% MKDIR %LogFolder%

REM --- Start Capture ---
echo Starting Wireshark capture on interface %Interface% 
REM with filter %CaptureFilter%
echo Saving to: %LogFolder%\%FileName%

REM The -w flag specifies the output file location and name
REM The -f flag specifies the capture filter
REM The -q flag suppresses output to the console (optional, remove for real-time packet count)
REM The -a duration:value or -b options can be used for automatic stop/ring buffer management (optional)

%WiresharkPath% -i %Interface% -w %LogFolder%\%FileName%
REM Example with ring buffer: captures 5 files, 10MB each, switches files after 1 hour (3600 secs) or 10000 KB size
REM %WiresharkPath% -i %Interface% -f %CaptureFilter% -w %LogFolder%\%FileName% -b filesize:10000 -b files:5 -b duration:3600 -q

pause
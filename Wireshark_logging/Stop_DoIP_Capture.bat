@echo off
REM --- Stop Wireshark/tshark Capture Process ---

echo Attempting to stop any running tshark.exe processes...

REM Taskkill command:
REM /F forces termination
REM /IM specifies the Image Name (process name)

taskkill /F /IM tshark.exe

REM Check if the command was successful (ErrorLevel 0 means success)
IF %ERRORLEVEL% EQU 0 (
    echo tshark.exe process terminated successfully.
) ELSE (
    echo No tshark.exe process was found running, or an error occurred.
)

pause

@echo off
REM --- Configuration ---
SET SourceFolder="C:\Users\vcatstester\Desktop\Wireshark_Logging"
SET DestFolder=""
REM Filter for a specific extension, e.g., *.pcapng, *.log, or *.* for all files
SET FilePattern=*.pcapng 

REM Clear previous variables
SET MostRecentFile=
SET FullPathToRecentFile=
SET DestPath=

echo Searching for the most recent file in %SourceFolder%...

REM --- Find the Most Recent File ---
FOR /F "delims=" %%I IN ('dir %SourceFolder%\%FilePattern% /B /A:-D /O:-D') DO (
    REM Capture only the very first result from the newest-first list
    IF NOT DEFINED MostRecentFile (
        SET MostRecentFile=%%I
        GOTO :FoundRecentFile
    )
)

:FoundRecentFile
REM --- Check if a file was found and proceed with move operation ---

IF DEFINED MostRecentFile (
    echo.
    echo Found Most Recent File: "%MostRecentFile%"
    
    REM Define the full source and destination paths using the found filename
    SET FullPathToRecentFile=%SourceFolder%\%MostRecentFile%
    SET DestPath=%DestFolder%\%MostRecentFile%

    REM Ensure destination folder exists
    IF NOT EXIST %DestFolder% MKDIR %DestFolder%

    echo Moving "%FullPathToRecentFile%" to "%DestFolder%"

    REM Use MOVE for same-drive operations (automatically deletes source)
    MOVE %FullPathToRecentFile% %DestPath%
    
    REM Verification check after move
    IF EXIST %DestPath% (
        echo Success: File moved and original deleted.
    ) ELSE (
        echo Error during move operation.
    )

) ELSE (
    echo No files found matching the pattern %FilePattern% in %SourceFolder%.
)

pause

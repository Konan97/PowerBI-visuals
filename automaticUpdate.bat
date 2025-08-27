@echo off
:: automaticUpdate.bat
:: This script gets the latest update from SourceSafe

:: Set SourceSafe variables
:: "C:\Users\BPPSWCHS\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Microsoft Visual Studio 6.0\Microsoft Visual SourceSafe\Microsoft Visual SourceSafe 6.0.lnk"
set VSS_PATH="C:\Users\BPPSWCHS\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Microsoft Visual Studio 6.0\Microsoft Visual SourceSafe\Microsoft Visual SourceSafe 6.0.lnk"
set VSS_DB="\\gbw9061106.got.volvocars.net\proj\9413-shr-vcc50000\VCATS Source Safe VCC"
::"\\gbw9061106.got.volvocars.net\proj\9413-shr-vcc50000\VCATS Source Safe VCC"
set VSS_USER=Admin
set VSS_PASS=ngsdet
set VSS_PROJECT="$/VCC ELECTRICAL TESTING AND SWDL"
set LOCAL_DIR="C:\GRADEX"

:: Get latest version
%VSS_PATH% Get %VSS_PROJECT% -R -I- -O- -W -GL%LOCAL_DIR% -Y%VSS_USER%,%VSS_PASS% -D%VSS_DB%

:: End of script
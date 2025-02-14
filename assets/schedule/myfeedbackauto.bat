@echo off
tasklist /FI "IMAGENAME eq feedback.exe" 2>NUL | find /I "feedback.exe" >NUL
if %ERRORLEVEL% NEQ 0 (
    start /min "" "C:\user feedback\feedback\feedback.exe"
)
exit

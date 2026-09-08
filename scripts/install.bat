@echo off
cd /d "%~dp0.."
py -3 installer.py
if errorlevel 1 python installer.py
pause

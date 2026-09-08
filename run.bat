@echo off
cd /d "%~dp0"
py -3 runner.py
if errorlevel 1 python runner.py
pause

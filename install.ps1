$ErrorActionPreference='Stop'
Set-Location $PSScriptRoot
if (Get-Command py -ErrorAction SilentlyContinue) { py -3 installer.py } else { python installer.py }

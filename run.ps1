$ErrorActionPreference='Stop'
Set-Location $PSScriptRoot
if (Get-Command py -ErrorAction SilentlyContinue) { py -3 runner.py } else { python runner.py }

# PowerShell helper to create venv and install requirements
$root = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $root

if (-not (Test-Path .venv)) {
    python -m venv .venv
}

. .\.venv\Scripts\Activate.ps1
python -m pip install -U pip setuptools wheel
if (Test-Path requirements.txt) {
    python -m pip install -r requirements.txt
}
Write-Host "Environment ready. Activate with: .\.venv\Scripts\Activate.ps1"

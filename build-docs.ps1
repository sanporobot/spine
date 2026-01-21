$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$docs = Join-Path $root "docs"
$venv = Join-Path $root ".venv"

if (-not (Test-Path $venv)) {
    Write-Error "Missing venv at $venv. Create it first: python3 -m venv .venv"
    exit 1
}

& "$venv\Scripts\Activate.ps1"

python3 -m pip install -r "$docs\requirements.txt"

python3 -m sphinx -b html -D language=zh_CN -c $docs "$docs\zh" "$docs\_build\html\zh"
python3 -m sphinx -b html -D language=en -c $docs "$docs\en" "$docs\_build\html\en"

Write-Host "Build complete:"
Write-Host "  $docs\_build\html\zh"
Write-Host "  $docs\_build\html\en"

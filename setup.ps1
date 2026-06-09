<#
.SYNOPSIS
  Quick re-setup for Personal Coach — checks & installs everything.
#>

$ErrorActionPreference = "Continue"
$ROOT = Split-Path -Parent $PSCommandPath
$PYTHON = "C:\Users\Lenovo\AppData\Local\Programs\Python\Python312\python.exe"

# ── helpers ────────────────────────────────────────────────────────────────
function Run {
    param([string]$Cmd, [string]$Desc)
    Write-Host ">>> $Desc" -ForegroundColor Cyan
    Invoke-Expression $Cmd 2>&1 | Out-Host
}

function Check-Installed {
    param([string]$Name, [string]$CheckCmd)
    $null = Invoke-Expression $CheckCmd 2>&1
    return $LASTEXITCODE -eq 0
}

function Install-Pip {
    param([string]$Req)
    if (Test-Path $Req) {
        Run "& $PYTHON -m pip install -r $Req -q" "Python deps from $(Split-Path -Leaf $Req)"
    }
}

# ── 1. Python ──────────────────────────────────────────────────────────────
Write-Host "`n====== 1. Python ======" -ForegroundColor Yellow
try {
    $ver = & $PYTHON --version 2>&1
    Write-Host "  $ver" -ForegroundColor Green
} catch {
    Write-Host "  Python not found at `"$PYTHON`". Install Python 3.12+ first." -ForegroundColor Red
    exit 1
}

# ── 2. Python packages ─────────────────────────────────────────────────────
Write-Host "`n====== 2. Python packages ======" -ForegroundColor Yellow
Install-Pip "$ROOT\coach\requirements.txt"

# ── 3. LightRAG (optional) ──────────────────────────────────────────────
Write-Host "`n====== 3. LightRAG (optional) ======" -ForegroundColor Yellow
try {
    $null = & $PYTHON -c "import lightrag; print(f'LightRAG v{lightrag.__version__}')" 2>&1
    Write-Host "  LightRAG OK" -ForegroundColor Green
} catch {
    Run "& $PYTHON -m pip install lightrag-hku -q" "Install LightRAG"
}

# ── 4. npm global tools ────────────────────────────────────────────────────
Write-Host "`n====== 4. npm global tools ======" -ForegroundColor Yellow
$npmTools = @{
    "n8n-mcp"   = "n8n-mcp"
    "uipro"     = "uipro"
}
foreach ($pkg in $npmTools.Keys) {
    $name = $npmTools[$pkg]
    try {
        $null = Get-Command $name -ErrorAction Stop
        Write-Host "  $name OK" -ForegroundColor Green
    } catch {
        Run "npm install -g $pkg" "Install $pkg globally"
    }
}

# ── 5. Claude plugins directory ────────────────────────────────────────────
Write-Host "`n====== 5. claude-mem ======" -ForegroundColor Yellow
$claudeMem = "$env:USERPROFILE\.claude\plugins\marketplaces\thedotmack\plugin"
if (Test-Path $claudeMem) {
    Write-Host "  claude-mem plugin directory exists" -ForegroundColor Green
} else {
    Run "npx claude-mem install --ide opencode --no-auto-start" "Install claude-mem for OpenCode"
}

# ── 6. Bun (for claude-mem worker) ─────────────────────────────────────────
Write-Host "`n====== 6. Bun runtime ======" -ForegroundColor Yellow
$bunPaths = @("$env:USERPROFILE\.bun\bin\bun.exe", "$env:LOCALAPPDATA\bun\bin\bun.exe")
$bunFound = $false
foreach ($bp in $bunPaths) {
    if (Test-Path $bp) {
        $bv = & $bp --version 2>$null
        Write-Host "  Bun v$bv at $bp" -ForegroundColor Green
        $bunFound = $true
        break
    }
}
if (-not $bunFound) {
    try {
        $null = Get-Command bun -ErrorAction Stop
        $bv = & bun --version
        Write-Host "  Bun v$bv" -ForegroundColor Green
        $bunFound = $true
    } catch {}
}
if (-not $bunFound) {
    Run "powershell -c `"irm bun.sh/install.ps1 | iex`"" "Install Bun"
}

# ── 7. Ollama check ────────────────────────────────────────────────────────
Write-Host "`n====== 7. Ollama ======" -ForegroundColor Yellow
try {
    $null = Invoke-WebRequest -Uri "http://localhost:11434/api/tags" -TimeoutSec 3 -ErrorAction Stop
    Write-Host "  Ollama running" -ForegroundColor Green
    $ollamaExe = if (Test-Path "$env:USERPROFILE\.ollama\ollama.exe") { "$env:USERPROFILE\.ollama\ollama.exe" } else { "ollama" }
    $models = (& $ollamaExe list 2>$null)
    Write-Host "  Models:" -ForegroundColor Cyan
    foreach ($m in @("llama3.2:3b", "bge-m3", "nomic-embed-text")) {
        if ($models -match $m) {
            Write-Host "    $m [OK]" -ForegroundColor Green
        } else {
            Run "ollama pull $m" "  Pull $m"
        }
    }
} catch {
    Write-Host "  Ollama not running. LightRAG will fall back to TF-IDF." -ForegroundColor Yellow
}

# ── 8. Rebuild memory index ────────────────────────────────────────────────
Write-Host "`n====== 8. Rebuild memory index ======" -ForegroundColor Yellow
Run "& $PYTHON $ROOT\coach\tools\index_memory_lightrag.py" "Build memory index (LightRAG/TF-IDF)"

# ── done ───────────────────────────────────────────────────────────────────
Write-Host "`n====== Done ======" -ForegroundColor Green
Write-Host "Personal Coach setup complete." -ForegroundColor Green
Write-Host "Run 'py -3 coach/tools/session_hooks.py pre' to verify." -ForegroundColor Cyan

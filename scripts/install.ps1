param(
  [switch]$DryRun,
  [switch]$ForceConfig
)

$ErrorActionPreference = "Stop"
$Root = Resolve-Path (Join-Path $PSScriptRoot "..")
$CodexHome = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME ".codex" }
$BackupDir = Join-Path $CodexHome ("backups/" + (Get-Date -Format "yyyyMMdd-HHmmss"))

function Invoke-Step {
  param([scriptblock]$Action, [string]$Text)
  if ($DryRun) {
    Write-Host "[dry-run] $Text"
  } else {
    & $Action
  }
}

function Backup-Path {
  param([string]$Path, [string]$Rel)
  if (Test-Path $Path) {
    $Target = Join-Path $BackupDir $Rel
    Invoke-Step { New-Item -ItemType Directory -Force -Path (Split-Path $Target) | Out-Null } "mkdir $(Split-Path $Target)"
    Invoke-Step { Copy-Item -Recurse -Force $Path $Target } "copy $Path $Target"
  }
}

function Copy-ConfigFile {
  param([string]$Name)
  $Src = Join-Path $Root $Name
  $Dst = Join-Path $CodexHome $Name
  if (Test-Path $Src) {
    Backup-Path $Dst $Name
    Invoke-Step { New-Item -ItemType Directory -Force -Path (Split-Path $Dst) | Out-Null } "mkdir $(Split-Path $Dst)"
    Invoke-Step { Copy-Item -Force $Src $Dst } "copy $Src $Dst"
  }
}

Invoke-Step { New-Item -ItemType Directory -Force -Path $CodexHome | Out-Null } "mkdir $CodexHome"

@(
  "AGENTS.md",
  "RTK.md",
  "WORKFLOW.md",
  "VERIFY.md",
  "SKILLS_POLICY.md",
  "SPEC_DESIGN.md",
  "EVAL_DESIGN.md",
  "DIFF_REVIEW.md",
  "TOKENOMICS.md",
  "SKILL_PRUNING.md"
) | ForEach-Object { Copy-ConfigFile $_ }

$SkillsSrc = Join-Path $Root "skills"
$SkillsDst = Join-Path $CodexHome "skills"
if (Test-Path $SkillsSrc) {
  Backup-Path $SkillsDst "skills"
  Invoke-Step { Copy-Item -Recurse -Force $SkillsSrc $SkillsDst } "copy $SkillsSrc $SkillsDst"
}

$TemplateSrc = Join-Path $Root "config/config.toml.template"
$TemplateDst = Join-Path $CodexHome "config.toml.template"
Backup-Path $TemplateDst "config.toml.template"
Invoke-Step { Copy-Item -Force $TemplateSrc $TemplateDst } "copy $TemplateSrc $TemplateDst"

$ConfigDst = Join-Path $CodexHome "config.toml"
if ($ForceConfig -or -not (Test-Path $ConfigDst)) {
  Backup-Path $ConfigDst "config.toml"
  Invoke-Step { Copy-Item -Force $TemplateSrc $ConfigDst } "copy config template to $ConfigDst"
} else {
  Write-Host "config.toml preserved; use -ForceConfig to replace it."
}

Write-Host "install complete: $CodexHome"
Write-Host "backup: $BackupDir"

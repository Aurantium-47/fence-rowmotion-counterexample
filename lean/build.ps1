param(
  [string]$LeanExecutable = 'lean',
  [string]$DependencyPackages = ''
)
$ErrorActionPreference = 'Stop'
$projectRoot = $PSScriptRoot
if ([string]::IsNullOrWhiteSpace($DependencyPackages)) {
  $DependencyPackages = Join-Path $projectRoot '.lake/packages'
}
$resolvedLean = (Get-Command $LeanExecutable -ErrorAction Stop).Source
$versionText = & $resolvedLean --version
if ($LASTEXITCODE -ne 0 -or $versionText -notmatch 'version 4\.19\.0,.*commit 6caaee842e94') {
  throw 'The build requires the pinned Lean 4.19.0 release.'
}
$manifest = Get-Content -LiteralPath (Join-Path $projectRoot 'lake-manifest.json') -Raw | ConvertFrom-Json
$dependencyLibs = @()
foreach ($dependency in $manifest.packages) {
  $dependencyRoot = Join-Path $DependencyPackages $dependency.name
  if (-not (Test-Path -LiteralPath $dependencyRoot)) { throw "Missing dependency: $($dependency.name)" }
  $actualRevision = & git -C $dependencyRoot rev-parse HEAD 2>$null
  if ($LASTEXITCODE -ne 0 -or $actualRevision -ne $dependency.rev) {
    throw "Dependency revision mismatch: $($dependency.name)"
  }
  $dependencyLib = Join-Path $dependencyRoot '.lake/build/lib/lean'
  if (Test-Path -LiteralPath $dependencyLib) { $dependencyLibs += $dependencyLib }
  Write-Output "PIN $($dependency.name) $actualRevision"
}
$localLib = Join-Path $projectRoot '.lake/build/lib/lean'
New-Item -ItemType Directory -Force -Path (Join-Path $localLib 'W04') | Out-Null
$previousLeanPath = $env:LEAN_PATH
$env:LEAN_PATH = (@($localLib, $projectRoot) + $dependencyLibs) -join [System.IO.Path]::PathSeparator
Push-Location $projectRoot
try {
  foreach ($module in @('Poset', 'Rowmotion', 'Orbit', 'Main')) {
    Write-Output "BUILD W04/$module.lean with $versionText"
    & $resolvedLean -j 2 -s 131072 -o ".lake/build/lib/lean/W04/$module.olean" "W04/$module.lean"
    if ($LASTEXITCODE -ne 0) { throw "Lean failed for W04/$module.lean with exit code $LASTEXITCODE" }
    Write-Output "PASS W04/$module.lean"
  }
  Write-Output 'BUILD W04.lean'
  & $resolvedLean -j 2 -s 131072 -o '.lake/build/lib/lean/W04.olean' 'W04.lean'
  if ($LASTEXITCODE -ne 0) { throw "Lean failed for W04.lean with exit code $LASTEXITCODE" }
  Write-Output 'PASS W04.lean'
  Write-Output 'BUILD RESULT: SUCCESS'
} finally {
  Pop-Location
  $env:LEAN_PATH = $previousLeanPath
}

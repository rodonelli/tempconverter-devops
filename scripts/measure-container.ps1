param(
    [string]$OutputDirectory = 'resource-results',
    [int]$Samples = 12,
    [int]$IntervalSeconds = 5
)

$ErrorActionPreference = 'Stop'
New-Item -ItemType Directory -Force -Path $OutputDirectory | Out-Null
$OutputFile = Join-Path $OutputDirectory 'container-stats.csv'
'timestamp,name,cpu_percent,memory_usage,processes' | Set-Content $OutputFile

for ($i = 0; $i -lt $Samples; $i++) {
    $Timestamp = Get-Date -Format o
    podman stats --no-stream --format "$Timestamp,{{.Name}},{{.CPU}},{{.MemUsage}},{{.PIDs}}" | Add-Content $OutputFile
    Start-Sleep -Seconds $IntervalSeconds
}

Write-Host "Saved measurements to $OutputFile"

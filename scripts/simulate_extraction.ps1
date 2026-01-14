<#
.SYNOPSIS
Simulates a legacy system exporting files to the source directory.

.DESCRIPTION
Generates dummy files with various naming patterns (valid and invalid) to test the ETL pipeline's validation logic.

.PARAMETER Destination
The directory to drop files into. Defaults to ..\data\source
#>

param (
    [string]$Destination = "data\source"
)

$DestinationPath = Resolve-Path $Destination -ErrorAction SilentlyContinue
if (-not $DestinationPath) {
    Write-Host "Creating destination directory: $Destination"
    New-Item -ItemType Directory -Path $Destination | Out-Null
    $DestinationPath = Resolve-Path $Destination
}

Write-Host "Simulating Legacy Data Export to: $DestinationPath"

# Helper to create a dummy file
function Create-DummyFile ($Name, $Content) {
    $FilePath = Join-Path $DestinationPath $Name
    Set-Content -Path $FilePath -Value $Content
    Write-Host "Created: $Name"
}

# 1. Valid Pattern: ID_TYPE_DATE.ext
Create-DummyFile "1001_LAB_20231025.pdf" "Dummy Lab Report Content"
Create-DummyFile "1002_XR_20231025.jpg" "Dummy X-Ray Image Content"
Create-DummyFile "1003_INV_20231026.pdf" "Dummy Invoice Content"

# 2. Invalid Pattern: Missing ID or Date
Create-DummyFile "LAB_REPORT_FINAL.pdf" "Invalid Name Format"
Create-DummyFile "unknown_file.txt" "Unknown file type"

# 3. Wrong Extension / Type Mismatch Logic (Simulated by content)
Create-DummyFile "1004_LAB_20231025.txt" "This should be a PDF usually?"

Write-Host "Simulation Complete. 6 files created."

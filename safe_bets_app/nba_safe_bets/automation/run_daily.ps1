# Run_Daily.ps1
# PowerShell automation script for NBA Safe Bets

$root = Split-Path -Parent $MyInvocation.MyCommand.Definition
Write-Host "Running NBA Daily Predictions from $root"

# (Optional) If using a virtual environment:
# & "$root\venv\Scripts\Activate.ps1"

# Run prediction engine
Write-Host "Running prediction engine..."
$python = "python"   # modify if python is installed differently

& $python "$root\..\daily_predict\daily_predict.py" | Tee-Object "$root\last_run.log"

Write-Host "Daily predictions complete."

# Export results
Write-Host "Exporting results..."
& $python "$root\export_results.py"

Write-Host "All tasks complete."

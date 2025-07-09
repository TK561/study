# Claude Code データディレクトリの確認と設定スクリプト

Write-Host "Claude Code データディレクトリを確認しています..." -ForegroundColor Cyan

# 可能なパスをチェック
$possiblePaths = @(
    "$env:USERPROFILE\.config\claude",
    "$env:USERPROFILE\.claude",
    "$env:APPDATA\claude",
    "$env:LOCALAPPDATA\claude"
)

$foundPath = $null

foreach ($path in $possiblePaths) {
    Write-Host "確認中: $path" -ForegroundColor Yellow
    if (Test-Path "$path\projects") {
        $foundPath = $path
        Write-Host "✓ 見つかりました: $path\projects" -ForegroundColor Green
        break
    }
}

if (-not $foundPath) {
    Write-Host "`nClaude Codeのデータディレクトリが見つかりません。" -ForegroundColor Red
    Write-Host "WSLを使用している場合は、以下のコマンドを試してください:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "# WSL内でのパスを確認" -ForegroundColor Cyan
    Write-Host 'wsl -e bash -c "find ~ -name claude -type d 2>/dev/null"'
    Write-Host ""
    Write-Host "# 見つかったパスを環境変数に設定（例）" -ForegroundColor Cyan
    Write-Host '$env:CLAUDE_CONFIG_DIR = "\\wsl$\Ubuntu\home\username\.config\claude"' -ForegroundColor White
    Write-Host ""
} else {
    Write-Host "`n環境変数を設定します..." -ForegroundColor Cyan
    $env:CLAUDE_CONFIG_DIR = $foundPath
    Write-Host "✓ CLAUDE_CONFIG_DIR = $foundPath" -ForegroundColor Green
    
    Write-Host "`nccusageを実行します..." -ForegroundColor Cyan
    npx ccusage@latest blocks
}

Write-Host "`n永続的に設定する場合は、以下のコマンドを実行してください:" -ForegroundColor Yellow
if ($foundPath) {
    $cmd = "[Environment]::SetEnvironmentVariable('CLAUDE_CONFIG_DIR', '$foundPath', 'User')"
    Write-Host $cmd -ForegroundColor White
}
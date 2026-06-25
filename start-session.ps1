# Start a personal-coach session with full context
Write-Host "=== Loading session context ===" -ForegroundColor Cyan
py -3 coach/tools/session_hooks.py pre
py -3 coach/tools/read_context.py 10
Write-Host "=== Context loaded. Starting opencode ===" -ForegroundColor Green
opencode

@echo off
set "DIR=%~dp0"
cd /d "%DIR%../minerl/MCP-Reborn"

patch -s -p 1 -i "%DIR%mcp_patch.diff"
:: Copy cursors over
xcopy "%DIR%\cursors" ".\src\main\resources\cursors" /E /I /Y

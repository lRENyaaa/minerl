@echo off
set "DIR=%~dp0../minerl"
cd /d "%DIR%"

rmdir /s /q MCP-Reborn
git clone https://github.com/Hexeption/MCP-Reborn.git
cd MCP-Reborn
git checkout 1.16.5-20210115
.\gradlew.bat setup
:: Clean up for patching
rmdir /s /q .git
rmdir /s /q run
rmdir /s /q projects
rmdir /s /q build
rmdir /s /q .gradle
del /q .gitignore
rmdir /s /q .github
del /q README.md

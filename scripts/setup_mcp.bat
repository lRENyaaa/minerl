@echo off
set "DIR=%~dp0../minerl"
cd /d "%DIR%"

rmdir /s /q MCP-Reborn
call setproxy.bat
git clone https://github.com/Hexeption/MCP-Reborn.git
cd MCP-Reborn
git checkout 1.16.5-20210115
set JAVA_HOME=C:\Program Files\Zulu\zulu-8\
set GRADLE_OPTS=-Dhttp.proxyHost=127.0.0.1 -Dhttp.proxyPort=10809 -Dhttps.proxyHost=127.0.0.1 -Dhttps.proxyPort=10809
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

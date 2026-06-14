@echo off
echo Installing EsoFur...

set SCRIPT_DIR=%~dp0
set SCRIPT_DIR_CLEAN=%SCRIPT_DIR:~0,-1%

:: ---- Create Command Prompt wrapper ----
(
    echo @echo off
    echo python "%SCRIPT_DIR%esofur" %%*
) > "%SCRIPT_DIR%esofur.bat"

:: ---- Create PowerShell wrapper ----
(
    echo python "%SCRIPT_DIR%esofur" $args
) > "%SCRIPT_DIR%esofur.ps1"

:: ---- Primary: copy to WindowsApps (already in User PATH, no restart needed) ----
copy /Y "%SCRIPT_DIR%esofur.bat" "%LOCALAPPDATA%\Microsoft\WindowsApps\esofur.bat" >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo Installed to WindowsApps - esofur is ready to use immediately.
    goto done
)

:: ---- Fallback: add SCRIPT_DIR to User PATH via PowerShell ----
echo Could not write to WindowsApps, updating PATH instead...
set ESOFUR_INSTALL_DIR=%SCRIPT_DIR_CLEAN%
powershell -NoProfile -ExecutionPolicy Bypass -Command "$dir=$env:ESOFUR_INSTALL_DIR; $cur=[Environment]::GetEnvironmentVariable('PATH','User'); if(($cur -split ';') -notcontains $dir){ [Environment]::SetEnvironmentVariable('PATH',$cur+';'+$dir,'User'); Write-Host 'Added to PATH.' } else { Write-Host 'Already in PATH - skipping.' }"

if %ERRORLEVEL% neq 0 (
    echo Warning: Could not update PATH automatically.
    echo Please add the following folder to your PATH manually:
    echo %SCRIPT_DIR_CLEAN%
    goto done
)

echo PATH updated - please restart your terminal for changes to take effect.

:done
echo.
echo Installed successfully!
echo Try: esofur test.EsoFur
